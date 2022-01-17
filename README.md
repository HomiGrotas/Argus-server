![Build Status](https://github.com/HomiGrotas/server/workflows/tests/badge.svg)

# Info
High-school final project
Monitoring computers with ability to block unwanted website traffic

# Endpoints
## /parent
| Methods | Parameters                      | Auth   |
|---------|---------------------------------|--------|
| POST    | email<br> password<br> nickname | None   |
| GET     | None                            | Parent |
| PATCH   | email (optional)<br> password (optional)<br> nickname(optional) | Parent |
<br><br>

#### /parent/child_registration_token
| Methods | Parameters | Auth |
|---------|------------|------|
| GET     | None       | Parent
<br><br>

## /child
| Methods | Parameters                                  | Auth  |
|---------|---------------------------------------------|-------|
| POST    | mac_address<br> nickname <br> parent_token  | Token |
| GET     | id <br> field (optional)                    | Parent|
| PATCH   | id <br> nickname (optional) <br> blocked (optional) <br> usage_limits (optional)| Parent|
<br><br>

#### /child/activity
| Methods | Parameters           | Auth |
|---------|----------------------|------|
| POST    | None                 | Child
| GET     | id <br> amount       | Parent
<br><br>

#### /child/web_history
| Methods | Parameters | Auth |
|---------|------------|------|
| POST    | 
| GET     | 
| PATCH   |
<br><br>

## Others
#### /blocked_websites
| Methods | Parameters            | Auth |
|---------|-----------------------|------|
| POST    | id <br> domain  | Parent
| GET     | id                    | Parent/ Child
| DELETE  | child_id <br> domain  | Parent
<br><br>

#### /commands
| Methods | Parameters            | Auth |
|---------|-----------------------|------|
| POST    | id <br command> | Parent
| GET     | id                    | Parent/ Child
| DELETE  | child_id <br> command | Parent
<br><br>


## Protection levels
| Protection Level  | Number    | Description                   |
|-------------------|-----------|-------------------------------|
| NO                | 0         | No protection at all. All domains are allowed.
| MINIMAL           | 1         | Blocks customized domains
| NORMAL            | 2         | * Blocks domains from our saved list <br> * Customized domains
| HARD              | 3         | Blocks all web traffic

## Password format
## Available commands
