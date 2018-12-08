-- Player punt data
DROP TABLE IF EXISTS player_punt_data;
CREATE TABLE player_punt_data
(
    GSISID NUMERIC,
    Number TEXT,
    Position TEXT
);
COPY player_punt_data(GSISID, Number, Position)
FROM '/tmp/player_punt_data.csv' DELIMITER ',' CSV HEADER;

-- Game Data
DROP TABLE IF EXISTS game_data;
CREATE TABLE game_data
(
    GameKey NUMERIC,
    Season_Year NUMERIC,
    Season_Type TEXT,
    Week NUMERIC,
    Game_Date DATE,
    Game_Day TEXT,
    Game_Site TEXT,
    Start_Time TIME,
    Home_Team TEXT,
    HomeTeamCode TEXT,
    Visit_Team TEXT,
    VisitTeamCode TEXT,
    Stadium TEXT,
    StadiumType TEXT,
    Turf TEXT,
    GameWeather TEXT,
    Temperature NUMERIC,
    OutdoorWeather TEXT
);
COPY game_data(GameKey,Season_Year,Season_Type,Week,Game_Date,Game_Day,Game_Site,Start_Time,Home_Team,HomeTeamCode,Visit_Team,VisitTeamCode,Stadium,StadiumType,Turf,GameWeather,Temperature,OutdoorWeather)
FROM '/tmp/game_data.csv' DELIMITER ',' CSV HEADER;

-- Play information
DROP TABLE IF EXISTS play_information;
CREATE TABLE play_information
(
    Season_Year NUMERIC,
    Season_Type TEXT,
    GameKey NUMERIC,
    Game_Date DATE,
    Week NUMERIC,
    PlayID NUMERIC,
    Game_Clock TIME,
    YardLine TEXT,
    Quarter NUMERIC,
    Play_Type TEXT,
    Poss_Team TEXT,
    Home_Team_Visit_Team TEXT,
    Score_Home_Visiting TEXT,
    PlayDescription TEXT
);
COPY play_information(Season_Year,Season_Type,GameKey,Game_Date,Week,PlayID,Game_Clock,YardLine,Quarter,Play_Type,Poss_Team,Home_Team_Visit_Team,Score_Home_Visiting,PlayDescription)
FROM '/tmp/play_information.csv' DELIMITER ',' CSV HEADER;

-- Play Player Role Data
DROP TABLE IF EXISTS play_player_role_data;
CREATE TABLE play_player_role_data
(
    Season_Year NUMERIC,
    GameKey NUMERIC,
    PlayID NUMERIC,
    GSISID NUMERIC,
    Role TEXT
);
COPY play_player_role_data(Season_Year,GameKey,PlayID,GSISID,Role)
FROM '/tmp/play_player_role_data.csv' DELIMITER ',' CSV HEADER;

-- video footage control
DROP TABLE IF EXISTS video_footage_control;
CREATE TABLE video_footage_control
(
	season NUMERIC,
	Season_Type TEXT,
	Week NUMERIC,
	Home_team TEXT,
	Visit_Team TEXT,
	Qtr NUMERIC,
	PlayDescription TEXT,
	gamekey NUMERIC,
	playid NUMERIC,
	PreviewLink TEXT
);
COPY video_footage_control(season,Season_Type,Week,Home_team,Visit_Team,Qtr,PlayDescription,gamekey,playid,PreviewLink)
FROM '/tmp/video_footage-control.csv' DELIMITER ',' CSV HEADER;

-- video footage injury
DROP TABLE IF EXISTS video_footage_injury;
CREATE TABLE video_footage_injury
(
	season NUMERIC,
	Season_Type TEXT,
	Week NUMERIC,
	Home_team TEXT,
	Visit_Team TEXT,
	Qtr NUMERIC,
	PlayDescription TEXT,
	gamekey NUMERIC,
	playid NUMERIC,
	PreviewLink TEXT
);
COPY video_footage_injury(season,Season_Type,Week,Home_team,Visit_Team,Qtr,PlayDescription,gamekey,playid,PreviewLink)
FROM '/tmp/video_footage-injury.csv' DELIMITER ',' CSV HEADER;

-- video review data
DROP TABLE IF EXISTS video_review;
CREATE TABLE video_review
(
	Season_Year NUMERIC,
	GameKey NUMERIC,
	PlayID NUMERIC,
	GSISID NUMERIC,
	Player_Activity_Derived TEXT,
	Turnover_Related TEXT,
	Primary_Impact_Type TEXT,
	Primary_Partner_GSISID NUMERIC,
	Primary_Partner_Activity_Derived TEXT,
	Friendly_Fire TEXT
);
COPY video_review(Season_Year,GameKey,PlayID,GSISID,Player_Activity_Derived,Turnover_Related,Primary_Impact_Type,Primary_Partner_GSISID,Primary_Partner_Activity_Derived,Friendly_Fire)
FROM '/tmp/video_review.csv' DELIMITER ',' CSV HEADER;

-- NGS Data
DROP TABLE IF EXISTS ngs;
CREATE TABLE ngs
(
    Season_Year NUMERIC,
    GameKey NUMERIC,
    PlayID NUMERIC,
    GSISID NUMERIC,
    Time TIMESTAMP,
    x FLOAT,
    y FLOAT,
    dis NUMERIC,
    o NUMERIC,
    dir NUMERIC,
    Event TEXT
);
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2016-pre.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2017-pre.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2016-post.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2017-post.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2016-reg-wk1-6.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2017-reg-wk1-6.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2016-reg-wk7-12.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2017-reg-wk7-12.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2016-reg-wk13-17.csv' DELIMITER ',' CSV HEADER;
COPY ngs(Season_Year,GameKey,PlayID,GSISID,Time,x,y,dis,o,dir,Event)
FROM '/tmp/NGS-2017-reg-wk13-17.csv' DELIMITER ',' CSV HEADER;
