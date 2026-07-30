# Database Design

## Planet

- PlanetID
- Name
- Radius
- Mass
- Gravity
- Description
- ImageURL

---

## Educational_Content

- ContentID
- PlanetID
- Title
- Explanation
- Animation
- Facts

---

## Events

- EventID
- EventName
- EventDate
- EventType
- Description

---

## Query_Log

- QueryID
- Location
- Date
- Time
- SearchTimestamp

---

## Notes

Dynamic astronomical calculations such as:

- Planet Positions
- Moon Phase
- Rise and Set Times

will be computed using Skyfield instead of being permanently stored in the database.

The database stores only reusable and persistent information.