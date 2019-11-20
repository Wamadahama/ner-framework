-- entity tables 
create table EntityType (
       id integer primary key autoincrement,
       ModelId integer, 
       EntityName text NOT NULL
);

create table EntityAttributes (
       id integer primary key autoincrement,
       EntityTypeId integer NOT NULL, 
       AttributeName text NOT NULL,
       AttributeValue text NOT NULL 
);

create table Corpus (
       id integer primary key autoincrement,
       EntityType id integer NOT NULL, 
       RawText text NOT NULL 
);

create table ModelResult (
       id integer primary key autoincrement,
       EntityType id NOT NULL,
       ModelId int not null
);

create table Categorization (
       id integer primary key autoincrement,
       ModelResultId integer NOT NULL,
       EntityAttributesId integer NOT NULL,
       Word text NOT NULL,
       Certainty integer NOT NULL 
);

create table Model (
       id integer primary key autoincrement,
       ModelName text,
       ModelDescription text,
       Observations int
);

-- web page tables 
-- might need to add more tables that would drive the website 
