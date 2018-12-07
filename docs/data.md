# Kaggle Punt Data

The following data is provided for NFL seasons 2016 to 2017.

Each dataset can be merged on the game, play or player level using the provided key variables. GameKey provides a unique identifier for a specific game which is unique across NFL seasons. PlayID identifies a unique play within a specified GameKey. GSISID provides a unique identifier for a player across all seasons.

## File descriptions

- **Game Data**: Game level data that specifies the type of season (pre, reg, post), week, and hosting city and team. Each game is uniquely identified across all seasons using `GameKey`.
- **Play Information**: Play level data that describes the type of play, possession team, score and a brief narrative of each play. Plays are uniquely identified using a its `PlayID` along with the corresponding `GameKey`. `PlayIDs` are not unique.
- **Player Punt Data**: Player level data that specifies the traditional football position for each player. Each player is identified using his `GSISID`.
- **Play Player Role Data**: Play and player level data that specifies a punt specific player role. This dataset will specify each player that played in each play. A player’s role in a play is uniquely defined by the `Gamekey` `PlayID` and `GSISID`.
- **Video Review**: Injury level data that provides a detailed description of the concussion-producing event. Video Review data are only available in cases in which the injury play can be identified. Each video review case can be identified using a combination of `GameKey`, `PlayID`, and `GSISID`. A brief narrative of the play events is provided.
- **NGS**: Next Gen Stats – player level data that describes the movement of each player during a play. NGS data is processed by BIOCORE to produce relevant speed and direction data. The NGS data is identified using `GameKey`, `PlayID`, and `GSISID`. Player data for each play is provided as a function of time (Time) for the duration of the play.


