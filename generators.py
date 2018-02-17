# built-in
from collections import namedtuple
import csv
import os
# external
import sql


try:
    from mysql_mock import cursor
except ImportError:
    cursor = None


Table = namedtuple('Table', ['name', 'columns'])
Column = namedtuple('Column', ['field', 'values'])
Field = namedtuple('Field', ['name', 'dtype', 'null', 'length', 'uniq'])


class text(str):  #noQA
    pass

class dice(str):  #noQA
    pass


class BaseGenerator:
    falsy = ('0', '1', 'false', 'true')
    empty = ('null', 'none', '-', '')
    lengths = tuple(2 ** k for k in range(2, 9))

    def get_max_length(self, values, dtype):
        if dtype not in (str, dice):
            return 0
        length = max(map(len, values))
        return min(l for l in self.lengths if l >= length)

    def check_uniq(self, values):
        return len(values) == len(set(values))

    def get_types(self, values):
        for value in values:
            if value.lower() in self.falsy:
                yield bool
            elif value.lstrip('-').isdigit():
                yield int
            elif value.lstrip('-').replace('.', '').isdigit():
                yield float
            elif value.lower() in self.empty:
                yield None
            elif len(value) > 255:
                yield text
            elif value.replace('d', '').isdigit():
                yield dice
            else:
                yield str

    def detect_type(self, types):
        types = [t for t in types if t is not None]
        if all(map(lambda t: t is bool, types)):
            return bool
        if all(map(lambda t: t in (int, bool), types)):
            return int
        if all(map(lambda t: t in (float, int, bool), types)):
            return float
        if all(map(lambda t: t in (dice, float, int, bool), types)):
            return dice
        if all(map(lambda t: t in (str, dice, float, int, bool), types)):
            return str
        return text

    def convert_values(self, values, types, field_type):
        for value, value_type in zip(values, types):
            # null
            if value_type is None:
                yield None
            # bool
            elif field_type is bool:
                yield int(value in self.falsy)
            # other
            else:
                yield field_type(value)

    def parse(self, file_name):
        with open(file_name) as f:
            reader = csv.reader(f)
            for field_name, *values in zip(*reader):
                # types checking
                types = list(self.get_types(values))
                field_type = self.detect_type(types)
                # detect some params
                length = self.get_max_length(values, field_type)
                null = None in types
                uniq = not null and self.check_uniq(values)
                # convert
                field_name = field_name.lower().replace(' ', '_')
                values = self.convert_values(values, types, field_type)

                yield Column(
                    field=Field(
                        name=field_name,
                        dtype=field_type,
                        null=null,
                        length=length,
                        uniq=uniq,
                    ),
                    values=list(values),
                )

    def get_schema(self, dirname='csv/'):
        for file_name in os.listdir(dirname):
            yield Table(
                name=file_name[:-4],
                columns=list(self.parse(os.path.join(dirname, file_name))),
            )


class CreateGenerator(BaseGenerator):
    template_base = "CREATE TABLE `{table_name}` (\n\t{fields}\n);\n\n"
    template_field = "`{name}` {dtype} /*{stype}*/ {null}"
    
    types_mapping = {
        float: 'FLOAT',
        int: 'INTEGER',
        str: 'VARCHAR({})',
        text: 'TEXT',
        dice: 'VARCHAR({})',
        bool: 'BIT',
    }

    def get_query(self, table):
        fields = []
        for column in table.columns:
            field_type = self.types_mapping[column.field.dtype]
            fields.append(self.template_field.format(
                name=column.field.name,
                dtype=field_type.format(column.field.length),
                stype=column.field.dtype.__name__,
                null='NULL' if column.field.null else 'NOT NULL',
            ))
        return self.template_base.format(
            table_name=table.name,
            fields=',\n\t'.join(fields),
        )

    def generate(self):
        with open('sql/create.sql', 'w') as f:
            for table in self.get_schema():
                f.write(self.get_query(table))


class InsertGenerator(BaseGenerator):
    def generate(self):
        for table in self.get_schema():
            qtable = sql.Table(table.name)

            fields = [getattr(qtable, column.field.name) for column in table.columns]
            columns = [column.values for column in table.columns]

            with open('sql/insert_{}.template.sql'.format(table.name), 'w') as f:
                q = qtable.insert(columns=fields, values=[[0] * len(fields)])
                print(str(q), file=f)

            if cursor:
                with open('sql/insert_{}.mysql.sql'.format(table.name), 'w') as f:
                    for values in zip(*columns):
                        q = qtable.insert(columns=fields, values=[values])
                        print(cursor.mogrify(str(q), q.params), file=f)


if __name__ == '__main__':
    CreateGenerator().generate()
    InsertGenerator().generate()
