DROP TABLE IF EXISTS cyber_attacks;


CREATE TABLE cyber_attacks(
	id		serial primary key,
	date		timestamp,
	author		text,
	target		text,
	description 	text,
	attack		text,
	target_class	text,
	attack_class	text,
	country 	text,
	link 		text,
	tags		text);
