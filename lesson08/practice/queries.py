class Query:
    sql_get_all_goods = """select g.*, c.category_name from goods g left join category c on g.category_id = c.id"""

    sql_get_goods_condition = sql_get_all_goods + ' where 1=1 {condition}'

    sql_get_goods_by_id = sql_get_goods_condition.format(condition=' and g.id=?')

    sql_get_goods_by_category_id = sql_get_goods_condition.format(condition=' and g.category_id=?')

    sql_get_category = 'select * from category'

    sql_delete_item_by_id = 'delete from goods where id=?'

    sql_create_category = 'insert into category (category_name) VALUES (?)'

    sql_delete_category_by_id = 'delete from category where id=?'

    sql_delete_goods_by_category_id = 'delete from goods where category_id=?'

    sql_create_goods_item = 'insert into goods (category_id, article_name, barcode, description, is_present, price, stock) VALUES (?, ?, ?, ?, ?, ?, ?)'
