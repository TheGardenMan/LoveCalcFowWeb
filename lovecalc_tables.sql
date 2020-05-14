create table link_owners (owner_id serial primary key ,owner_name text,secret_hash_of_owner text,create_time timestamptz);
create table crushlist(owner_id integer,user_name text,crush_name text,create_time timestamptz);
insert into link_owners(owner_name,secret_hash_of_owner) values('xx','xx');
SELECT COUNT(secret_hash_of_owner) FROM link_owners where secret_hash_of_owner='bb21d47900097b52' limit 1;