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
| PATCH   | email<br> password<br> nickname | Parent |
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
| GET     | nickname <br> field (optional)              | Parent|
| PATCH   | current_nickname <br> nickname <br> blocked | Parent|
<br><br>

#### /child/activity
| Methods | Parameters           | Auth |
|---------|----------------------|------|
| POST    | None                 | Child
| GET     | nickname <br> amount | Parent
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
| POST    | nickname <br> domain  | Parent
| GET     | nickname              | Parent/ Child
| DELETE  | nickname <br> domain  | Parent
<br><br>

#### /commands
| Methods | Parameters            | Auth |
|---------|-----------------------|------|
| POST    | nickname <br command> | Parent
| GET     | nickname   |          | Parent/ Child
| DELETE  | nickname <br command> | Parent
<br><br>
