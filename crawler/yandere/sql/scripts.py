create_tb_tags = """CREATE TABLE IF NOT EXISTS tags ( 
            id                   integer  NOT NULL  ,
            name                 varchar(100)  NOT NULL  ,
            "count"              integer DEFAULT 0 NOT NULL  ,
            "type"               integer DEFAULT 0 NOT NULL  ,
            ambiguous            boolean DEFAULT False   ,
            created_at           varchar(100)    ,
            updated_at           varchar(100)    ,
            note                 text    ,
            CONSTRAINT pk_tags PRIMARY KEY ( id )
         );"""
