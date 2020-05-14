import random
import psycopg2
import xxhash
hash_gen=xxhash.xxh64(seed=8745109705)
isError=False
cursor="blah"

try:
	connection = psycopg2.connect(user = "postgres",
								  password = "jaxtek",
								  host = "127.0.0.1",
								  port = "5432",
								  database = "postgres")
	cursor = connection.cursor()

except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)
	isError=True

def register_owner(owner_name):
	try:
		hash_gen.update(''.join([str(owner_name),str(random.randint(1,1000000)) ]))
		hash_of_owner_name=hash_gen.hexdigest()
		cursor.execute("insert into link_owners(owner_name,secret_hash_of_owner,create_time) values(%s,%s,current_timestamp) returning owner_id",(owner_name,hash_of_owner_name))
		owner_id=cursor.fetchone()
		owner_id=owner_id[0]
		print(owner_id,"   <--owner_id created ")
		connection.commit()
		return None,hash_of_owner_name,owner_id
	except Exception as e:
		print(e)
		connection.commit()
		return e,hash_of_owner_name,"No owner_id "

def add_crush(owner_id,user_name,crush_name):
	cursor.execute("insert into crushlist(owner_id,user_name,crush_name,create_time) values(%s,%s,%s,current_timestamp)",(owner_id,user_name,crush_name,))
	connection.commit()

def get_crush(owner_id):
	cursor.execute("select user_name,crush_name from crushlist where owner_id=%s order by create_time desc;",(owner_id,))
	x=cursor.fetchall()
	users_and_crushes=[]
	for n,e in enumerate(x):
		user_and_crush=[]
		user_and_crush.insert(0,e[0])
		user_and_crush.insert(1,e[1])
		users_and_crushes.insert(n,user_and_crush)
	print(users_and_crushes)
	return users_and_crushes

def if_hash_exists(secret_hash_of_owner):
	cursor.execute("SELECT COUNT(secret_hash_of_owner) FROM link_owners where secret_hash_of_owner=%s limit 1 ",(secret_hash_of_owner,))
	count=cursor.fetchone();
	count=int(count[0])
	# print(count,"count")
	if count>0:
		return True
	else:
		return False
def get_owner_id_name(secret_hash_of_owner):
	cursor.execute("SELECT owner_id,owner_name from link_owners where secret_hash_of_owner=%s limit 1",(secret_hash_of_owner,))
	data=cursor.fetchone()
	# print(owner_id)
	owner_id=int(data[0])
	owner_name=str(data[1])
	print(owner_name,owner_id)
	return owner_id,owner_name

def get_owner_name(owner_id):
	cursor.execute("SELECT owner_name from link_owners where owner_id=%s limit 1",(owner_id,))
	data=cursor.fetchone()
	owner_name=data[0]
	return owner_name

