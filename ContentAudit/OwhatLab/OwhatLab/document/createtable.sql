create  database test_OwhatLab;

create  table  user_info(
user_id  int(11) DEFAULT NULL,
nick_name varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
pic_url varchar(256) COLLATE utf8mb4_bin DEFAULT NULL,
update_time  int(11) DEFAULT NULL
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='Owhat Lab用户信息表';


create  table  article_info(
article_id int(11) DEFAULT NULL,
publish_time  int(11) DEFAULT NULL,
title  varchar(512)  DEFAULT NULL,
article_imgurl varchar(256) COLLATE utf8mb4_bin DEFAULT NULL,
column_id  varchar(64) DEFAULT NULL,
column_name varchar(20) DEFAULT NULL,
publisher_id  int(11) DEFAULT NULL,
publisher_name varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
publisher_pic_url varchar(256) COLLATE utf8mb4_bin DEFAULT NULL,
update_time  int(11) DEFAULT NULL
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='Owhat Lab文章信息表';



create  table  shop_info(
shop_id int(11) DEFAULT NULL,
publish_time  int(11) DEFAULT NULL,
title  varchar(512)  DEFAULT NULL,
shop_imgurl varchar(256) COLLATE utf8mb4_bin DEFAULT NULL,
column_id  varchar(64) DEFAULT NULL,
column_name varchar(20) DEFAULT NULL,
shop_max_price varchar(20) DEFAULT NULL,
shop_min_price varchar(20) DEFAULT NULL,
shop_sale_total varchar(20) DEFAULT NULL,
publisher_id  int(11) DEFAULT NULL,
publisher_name varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
publisher_pic_url varchar(256) COLLATE utf8mb4_bin DEFAULT NULL,
update_time  int(11) DEFAULT NULL
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='Owhat Lab商品信息表';