-- entity tables 
create table EntityType (
       id integer primary key autoincrement,
       EntityName text NOT NULL,
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
       ModelName  text NOT NULL, -- might not need 
);

create table Categorization (
       id integer primary key autoincrement,
       ModelResultId integer NOT NULL,
       EntityAttributesId integer NOT NULL,
       Word text NOT NULL,
       Certainty integer NOT NULL 
);


-- web page tables 
-- might need to add more tables that would drive the website 
