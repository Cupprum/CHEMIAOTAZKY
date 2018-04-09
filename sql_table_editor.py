from sql_table_maker import jedlo_sql, create_func, drop_func, insert_manual_one_func, insert_all_func


print('create, drop, insert_all, insert_one')
what_to_do = input()

if what_to_do == 'create':
    create_func()

elif what_to_do == 'drop':
    drop_func()

elif what_to_do == 'insert_manual_one':
    insert_manual_one_func()

elif what_to_do == 'insert_all':
    insert_all_func()

print(jedlo_sql.query.all())
