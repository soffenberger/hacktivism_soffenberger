DROP TABLE IF EXISTS test;

CREATE TABLE test(
	id		serial primary key,
	screen_name 	text,
	created_time	timestamp,
	message_content	text,
	hashtags	text,
	symbols		text,
	trends		text,
	user_id		bigint REFERENCES users,
	user_mentions	text,
	keywords 	text,
	language	text
);
