delete from anonymous;
delete from haters1;
delete from haters2;
delete from haters3;
delete from nashi;
delete from lizard_squad;
delete from russia;
delete from users;

select setval('anonymous_seq', 1);
select setval('haters1_seq', 1);
select setval('users_user_id_seq', 1);
select setval('haters2_seq', 1);
select setval('haters3_seq', 1);
select setval('nashi_seq', 1);
select setval('lizard_seq', 1);
select setval('russia_seq',1);

