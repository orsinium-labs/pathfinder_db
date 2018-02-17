CREATE TABLE `level_ups` (
	`level` INTEGER /*int*/ NOT NULL,
	`feat` BIT /*bool*/ NOT NULL,
	`ability` BIT /*bool*/ NOT NULL,
	`xp_slow` INTEGER /*int*/ NOT NULL,
	`xp_medium` INTEGER /*int*/ NOT NULL,
	`xp_fast` INTEGER /*int*/ NOT NULL
);

CREATE TABLE `sizes` (
	`name` VARCHAR(32) /*str*/ NOT NULL,
	`modif` INTEGER /*int*/ NOT NULL,
	`fly_modif` INTEGER /*int*/ NOT NULL,
	`stealth_modif` INTEGER /*int*/ NOT NULL,
	`space` FLOAT /*float*/ NOT NULL,
	`natural_reach` INTEGER /*int*/ NOT NULL,
	`height_min` FLOAT /*float*/ NOT NULL,
	`height_max` FLOAT /*float*/ NULL,
	`weight_min` FLOAT /*float*/ NOT NULL,
	`weight_max` FLOAT /*float*/ NULL
);

CREATE TABLE `aligments` (
	`abbr` VARCHAR(4) /*str*/ NOT NULL,
	`name` VARCHAR(16) /*str*/ NOT NULL,
	`lawful` BIT /*bool*/ NOT NULL,
	`chaotic` BIT /*bool*/ NOT NULL,
	`good` BIT /*bool*/ NOT NULL,
	`evil` BIT /*bool*/ NOT NULL
);

CREATE TABLE `skills_values` (
	`skill` VARCHAR(16) /*str*/ NOT NULL,
	`value` VARCHAR(16) /*str*/ NOT NULL
);

CREATE TABLE `genders` (
	`name` VARCHAR(8) /*str*/ NOT NULL
);

CREATE TABLE `descriptions` (
	`name` VARCHAR(32) /*str*/ NOT NULL,
	`descr` VARCHAR(256) /*str*/ NOT NULL
);

CREATE TABLE `skills` (
	`name` VARCHAR(16) /*str*/ NOT NULL,
	`stat` VARCHAR(4) /*str*/ NOT NULL,
	`armor` BIT /*bool*/ NOT NULL,
	`untrained` BIT /*bool*/ NOT NULL,
	`multi` BIT /*bool*/ NOT NULL
);

CREATE TABLE `base_damage_by_size` (
	`size` VARCHAR(32) /*str*/ NOT NULL,
	`bite` VARCHAR(4) /*dice*/ NOT NULL,
	`claw` VARCHAR(4) /*dice*/ NOT NULL,
	`gore` VARCHAR(4) /*dice*/ NOT NULL,
	`hoof` VARCHAR(4) /*dice*/ NOT NULL,
	`tentacle` VARCHAR(4) /*dice*/ NOT NULL,
	`wing` VARCHAR(4) /*dice*/ NOT NULL,
	`pincers` VARCHAR(4) /*dice*/ NOT NULL,
	`tail` VARCHAR(4) /*dice*/ NOT NULL,
	`slap` VARCHAR(4) /*dice*/ NOT NULL,
	`slam` VARCHAR(4) /*dice*/ NOT NULL,
	`sting` VARCHAR(4) /*dice*/ NOT NULL,
	`talons` VARCHAR(4) /*dice*/ NOT NULL,
	`other` VARCHAR(4) /*dice*/ NOT NULL
);

