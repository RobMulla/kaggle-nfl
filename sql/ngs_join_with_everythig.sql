SELECT ngs.*,
	   (ngs.dis * 20.4545) as mph,
	   pi.season_type,
	   pi.game_date,
	   pi.week,
	   pi.game_clock,
	   pi.yardline,
	   pi.quarter,
	   pi.play_type,
	   pi.poss_team,
	   pi.home_team_visit_team,
	   pi.score_home_visiting,
	   pi.playdescription,
	   REGEXP_REPLACE(COALESCE(pi.yardline, '0'), '[^0-9]*' ,'0')::integer as yard_int,
	   SUBSTRING(pi.home_team_visit_team, 1, 3) as home_team,
	   SUBSTRING(pi.home_team_visit_team, 5, 3) as away_team,
	   case when pi.poss_team = SUBSTRING(pi.home_team_visit_team, 1, 3) then 'home_poss' when pi.poss_team = SUBSTRING(pi.home_team_visit_team, 5, 3) then 'away_poss' else 'error' end as home_away_poss,
	   vr.player_activity_derived,
	   vr.turnover_related,
	   vr.primary_impact_type,
	   vr.gsisid as injured_gsisid,
	   vr.primary_partner_gsisid,
	   vr.primary_partner_activity_derived,
	   vr.friendly_fire
FROM ngs
LEFT JOIN play_information pi ON ngs.gamekey = pi.gamekey
AND ngs.playid = pi.playid
AND ngs.season_year = pi.season_year
LEFT JOIN video_review vr ON ngs.gamekey = vr.gamekey
AND ngs.season_year = vr.season_year
AND ngs.playid = vr.playid
LEFT JOIN video_footage_control vfc ON ngs.gamekey = vfc.gamekey
AND ngs.playid = vfc.playid
AND ngs.season_year = vfc.season
WHERE -- For testing
ngs.season_year = 2017 and
ngs.gamekey = 473 and
ngs.playid = 2072
limit 20;


SELECT ngs.*,
	   (ngs.dis * 20.4545) as mph,
	   pi.season_type,
	   pi.game_date,
	   pi.week,
	   pi.game_clock,
	   pi.yardline,
	   pi.quarter,
	   pi.play_type,
	   pi.poss_team,
	   pi.home_team_visit_team,
	   pi.score_home_visiting,
	   pi.playdescription,
	   REGEXP_REPLACE(COALESCE(pi.yardline, '0'), '[^0-9]*' ,'0')::integer as yard_int,
	   SUBSTRING(pi.home_team_visit_team, 1, 3) as home_team,
	   SUBSTRING(pi.home_team_visit_team, 5, 3) as away_team,
	   case when pi.poss_team = SUBSTRING(pi.home_team_visit_team, 1, 3) then 'home_poss' when pi.poss_team = SUBSTRING(pi.home_team_visit_team, 5, 3) then 'away_poss' else 'error' end as home_away_poss,
	   vr.player_activity_derived,
	   vr.turnover_related,
	   vr.primary_impact_type,
	   vr.gsisid as injured_gsisid,
	   vr.primary_partner_gsisid,
	   vr.primary_partner_activity_derived,
	   vr.friendly_fire,
	   ls_loc.gsisid as long_snapper_gsisid,
	   ls_loc.x as ls_x_when_line_set,
	   ls_loc.y as ls_y_when_line_set,
	   ls_loc.line_set_time as line_set_time
FROM ngs
LEFT JOIN play_information pi ON ngs.gamekey = pi.gamekey
AND ngs.playid = pi.playid
AND ngs.season_year = pi.season_year
LEFT JOIN video_review vr ON ngs.gamekey = vr.gamekey
AND ngs.season_year = vr.season_year
AND ngs.playid = vr.playid
LEFT JOIN video_footage_control vfc ON ngs.gamekey = vfc.gamekey
AND ngs.playid = vfc.playid
AND ngs.season_year = vfc.season
LEFT JOIN (SELECT ngs.season_year,
		   		ngs.gamekey,
		   		ngs.playid,
		   		ngs.gsisid,
		   		pprd.role,
		   		ngs.x,
		   		ngs.y,
		   		ngs.time as line_set_time
		   FROM ngs left join play_player_role_data pprd 
		   ON ngs.season_year = pprd.season_year AND
		   ngs.gamekey = pprd.gamekey AND
		   ngs.playid = pprd.playid AND
		   ngs.gsisid = pprd.gsisid
		   where ngs.event = 'line_set' and pprd.role = 'PLS') ls_loc
ON ngs.season_year = ls_loc.season_year AND
ngs.gamekey = ls_loc.gamekey AND
ngs.playid = ls_loc.playid
WHERE -- For testing
ngs.season_year = 2017 and
ngs.gamekey = 473 and
ngs.playid = 2072 and
ngs.gsisid = 32320;
