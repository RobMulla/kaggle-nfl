-- Joining video review with ngs data

from video_review vr
left join ngs on
	vr.primary_partner_gsisid = ngs.gsisid AND
	vr.gamekey = ngs.gamekey AND
	vr.season_year = ngs.season_year and
	vr.playid = ngs.playid
left join play_information ply on
	vr.gamekey = ply.gamekey and
	vr.season_year = ply.season_year and
	vr.playid = ply.playid
where vr.playid = 1212;


-- players involved in play

select vr.playid,
	   vr.season_year,
	   vr.gamekey,
	   vr.gsisid as hurt_player_id,
	   vr.primary_partner_gsisid as partner_player_id,
	   vr.primary_impact_type
from video_review vr;

--avg
select
	ngs.season_year,
	ngs.gamekey,
	ngs.playid,
	ngs.gsisid,
	min(ngs.time) as min_time,
	max(ngs.time) as max_time,
	round(avg(dis), 2) as avg_dis,
	round(avg(dis * 20.4545), 2) as avg_mph
from ngs
where
	ngs.season_year = 2016 and
	ngs.gamekey = 5 and
	ngs.playid = 3129
group by
	ngs.season_year,
	ngs.gamekey,
	ngs.playid,
	ngs.gsisid;

-- avg with player positions
select
	ngs.season_year,
	ngs.gamekey,
	ngs.playid,
	ngs.gsisid,
	min(ngs.time) as min_time,
	max(ngs.time) as max_time,
	round(avg(dis), 2) as avg_dis,
	round(avg(dis * 20.4545), 2) as avg_mph,
	player.role
from ngs
join play_player_role_data player
on ngs.season_year = player.season_year and
	ngs.gamekey = player.gamekey and
	ngs.gsisid = player.gsisid and
	ngs.playid = player.playid
where
	ngs.season_year = 2016 and
	ngs.gamekey = 5 and
	ngs.playid = 3129
group by
	ngs.season_year,
	ngs.gamekey,
	ngs.playid,
	ngs.gsisid,
	player.role;

-- more stuff
select
	ngs.season_year,
	ngs.gamekey,
	ngs.playid,
	ngs.gsisid,
	min(ngs.time) as min_time,
	max(ngs.time) as max_time,
	round(avg(dis), 2) as avg_dis,
	round(avg(dis * 20.4545), 2) as avg_mph,
	player.role,
	vr.friendly_fire,
	vr2.friendly_fire
from ngs
join play_player_role_data player
on ngs.season_year = player.season_year and
	ngs.gamekey = player.gamekey and
	ngs.gsisid = player.gsisid and
	ngs.playid = player.playid
left join video_review vr
on ngs.season_year = vr.season_year and
   ngs.gamekey = vr.gamekey and
   ngs.playid = vr.playid and
   ngs.gsisid = vr.gsisid
left join video_review vr2
on ngs.season_year = vr2.season_year and
   ngs.gamekey = vr2.gamekey and
   ngs.playid = vr2.playid and
   ngs.gsisid = vr2.primary_partner_gsisid
where
	ngs.season_year = 2016 and
	ngs.gamekey = 5 and
	ngs.playid = 3129
group by
	ngs.season_year,
	ngs.gamekey,
	ngs.playid,
	ngs.gsisid,
	player.role,
	vr.friendly_fire,
	vr2.friendly_fire;

-- More info on specific play

select
	ngs.season_year,
	ngs.gamekey,
	ngs.playid,
	ngs.gsisid,
	min(ngs.time) as min_time,
	max(ngs.time) as max_time,
	round(avg(dis), 2) as avg_dis,
	round(avg(dis * 20.4545), 2) as avg_mph,
	round(max(dis * 20.4545), 2) as max_mph,
	round(min(dis * 20.4545), 2) as min_mph,
	player.role,
	vr.friendly_fire,
	vr2.friendly_fire as friendly_fire_pp,
	vr.player_activity_derived as activity,
	vr2.primary_partner_activity_derived as partner_activity,
	pi.*
from ngs
join play_player_role_data player
on ngs.season_year = player.season_year and
	ngs.gamekey = player.gamekey and
	ngs.gsisid = player.gsisid and
	ngs.playid = player.playid
left join video_review vr
on ngs.season_year = vr.season_year and
   ngs.gamekey = vr.gamekey and
   ngs.playid = vr.playid and
   ngs.gsisid = vr.gsisid
left join video_review vr2
on ngs.season_year = vr2.season_year and
   ngs.gamekey = vr2.gamekey and
   ngs.playid = vr2.playid and
   ngs.gsisid = vr2.primary_partner_gsisid
left join play_information pi
on 
	ngs.season_year = pi.season_year AND
	ngs.gamekey = pi.gamekey AND
	ngs.playid = pi.playid
where
	ngs.season_year = 2016 and
	ngs.gamekey = 5 and
	ngs.playid = 3129
group by
	ngs.season_year,
	ngs.gamekey,
	ngs.playid,
	ngs.gsisid,
	player.role,
	vr.friendly_fire,
	vr2.friendly_fire,
	vr.player_activity_derived,
	vr2.primary_partner_activity_derived,
	vr.turnover_related,
	pi.season_year,
	pi.season_type,
	pi.gamekey,
	pi.game_date,
	pi.week,
	pi.playid,
	pi.game_clock,
	pi.yardline,
	pi.quarter,
	pi.play_type,
	pi.poss_team,
	pi.home_team_visit_team,
	pi.score_home_visiting,
	pi.playdescription;

-- every event for a specific play, so we can trim before the snap and after the play ends

select *
from ngs
left join 
