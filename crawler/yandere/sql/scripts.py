create_tb_tags = """
CREATE TABLE IF NOT EXISTS tags ( 
	id                   integer  NOT NULL  ,
	name                 varchar(100)  NOT NULL  ,
	"count"              integer DEFAULT 0 NOT NULL  ,
	"type"               integer DEFAULT 0 NOT NULL  ,
	ambiguous            boolean DEFAULT False   ,
	created_at           varchar(100)    ,
	updated_at           varchar(100)    ,
	note                 text    ,
	CONSTRAINT pk_tags PRIMARY KEY ( id )
);
"""

create_tb_jobs = """
CREATE TABLE IF NOT EXISTS jobs ( 
	id                   serial  NOT NULL  ,
	tag                  varchar(100)  NOT NULL  ,
	download_path        varchar(100)  NOT NULL  ,
	total_pages          integer DEFAULT 1 NOT NULL  ,
	total_posts          integer DEFAULT 0 NOT NULL  ,
	last_page_downloaded integer    ,
	last_post_downloaded integer    ,
	last_run             varchar(100)    ,
	created_at           varchar(100)    ,
	updated_at           varchar(100)    ,
	CONSTRAINT pk_jobs PRIMARY KEY ( id )
);
"""
