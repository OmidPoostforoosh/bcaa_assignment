# For the security purpose the credentials locates in a separate python script
# For this approach the database has been implemented in ElephentSQK postgreSQL cloud base environment

def credentials() :
        POSTGRES_ADDRESS = 'isilo.db.elephantsql.com'
        POSTGRES_PORT = '5432'
        POSTGRES_USERNAME = 'kerlqmtr'
        POSTGRES_PASSWORD = '68BQ6fXHG3QQ8qpolcO1nQjDxZwSJrBO'
        POSTGRES_DBNAME = 'kerlqmtr'

        return ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                        password=POSTGRES_PASSWORD,
                                                                                        ipaddress=POSTGRES_ADDRESS,
                                                                                        port=POSTGRES_PORT,
                                                                                        dbname=POSTGRES_DBNAME))

