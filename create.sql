CREATE TABLE Countryes(
    Country VARCHAR2(50) NOT NULL,
    primary key(Country)
);


CREATE TABLE Cityes(
    City VARCHAR2(50) NOT NULL,
    StateName VARCHAR2(50) NOT NULL,
    Country VARCHAR2(50) NOT NULL
);

ALTER TABLE Cityes
ADD CONSTRAINT CountryForen
FOREIGN KEY (Country) REFERENCES COUNTRYES(Country)
ON DELETE CASCADE;

ALTER TABLE Cityes
ADD PRIMARY KEY(City,StateName,Country);

CREATE TABLE Streets(
    Street VARCHAR2(50) NOT NULL,
    City  VARCHAR2(50) NOT NULL,
    StateName VARCHAR2(50) NOT NULL,
    Country VARCHAR2(50) NOT NULL,
    StreetNumber NUMBER NULL,
    PRIMARY KEY(Street,City,Country)
);


ALTER TABLE Streets
ADD CONSTRAINT CountryForenStreet
FOREIGN KEY (Country) REFERENCES COUNTRYES(Country)
ON DELETE CASCADE;

ALTER TABLE streets
ADD CONSTRAINT cityforen
FOREIGN KEY (city,statename,country) REFERENCES cityes(city,statename,country)
ON DELETE CASCADE;


CREATE TABLE TMC(
    TMC DECIMAL NOT NULL PRIMARY KEY
    );
CREATE TABLE Severityes(
    Severity INTEGER NOT NULL PRIMARY KEY
    );
CREATE TABLE Sources(
    InfoSource varchar2(50) NOT NULL PRIMARY KEY
    );

    
CREATE TABLE Sides(
    Side VARCHAR2(2) NOT NULL PRIMARY KEY
    );


ALTER SESSION SET NLS_TIMESTAMP_FORMAT='DD-MON-YY HH:MI:SSXFF';



CREATE TABLE INCEDENTS(
    ID INTEGER NOT NULL PRIMARY KEY,
    Street varchar2(50) NOT NULL,
    City  VARCHAR2(50) NOT NULL,
    Country VARCHAR2(50) NOT NULL,
    TMC FLOAT NULL,
    Severity INTEGER NOT NULL,
    InfoSource VARCHAR2(50) NOT NULL,
    StartTime TIMESTAMP NOT NULL,
    EndTime TIMESTAMP NOT NULL,
    Side VARCHAR2(1) NOT NULL,
    Distance FLOAT(10) NOT NULL,

    CONSTRAINT Incedent_Street_Foren
    FOREIGN KEY (Street,City,Country) REFERENCES streets(Street,City,Country),
    
    CONSTRAINT Incedent_TMC_Foren
    FOREIGN KEY (TMC) REFERENCES TMC(TMC),
    
    CONSTRAINT Incedent_Severity_Foren
    FOREIGN KEY (Severity) REFERENCES Severityes(Severity),
    
    CONSTRAINT Incedent_Source_Foren
    FOREIGN KEY (InfoSource) REFERENCES Sources(InfoSource),
    
    CONSTRAINT Incedent_Side_Foren
    FOREIGN KEY (Side) REFERENCES Sides(Side)
    
    );

CREATE SEQUENCE seq_incedents
MINVALUE 1
START WITH 1
INCREMENT BY 1
CACHE 10;


