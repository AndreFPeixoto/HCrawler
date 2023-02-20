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

create_tb_posts = """
CREATE TABLE IF NOT EXISTS posts ( 
	id                   integer  NOT NULL  ,
	tags                 text  NOT NULL  ,
	created_at           varchar(100)    ,
	author               varchar(100)    ,
	change               integer    ,
	"source"             text    ,
	score                integer    ,
	md5                  text    ,
	file_size            integer    ,
	file_ext             varchar(100)    ,
	file_url             text  NOT NULL  ,
	is_shown_in_index    boolean DEFAULT True   ,
	jpeg_url             text    ,
	jpeg_width           integer    ,
	jpeg_height          integer    ,
	jpeg_file_size       integer    ,
	rating               integer DEFAULT 0   ,
	is_rating_locked     boolean DEFAULT False   ,
	has_children         boolean DEFAULT False   ,
	parent_id            integer    ,
	status               varchar(100)    ,
	is_pending           boolean DEFAULT False   ,
	width                integer    ,
	height               integer    ,
	is_held              boolean DEFAULT False   ,
	downloaded           boolean DEFAULT True   ,
	downloaded_at        varchar(100)    ,
	downloaded_by        text    ,
	CONSTRAINT pk_posts PRIMARY KEY ( id )
);
"""
