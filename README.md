# datalayer
Datalayer

1. docker-compose up --build --no-cache
2. docker-compose down

## 1st run
| Operation                    | Postgres | MS SQL | Oracle | MySQL  | MariaDB | Cockroach |
| ---                    | --- | --- | --- | ---  | ---  | ---  |
| Researcher to Paper          | 0.162    | 0.253  | 0.117  | 0.077  |  0.614 | 0.021 |
| Researcher to Topic          | 0.137    | 0.213  | 0.088  | 0.003  |  0.218 | 0.050 |
| Researcher to Conference     | 0.162    | 0.200  | 0.121  | 0.049  |  0.207 | 0.201 |
| Researcher to Organization   | 0.162    | 0.206  | 0.122  | 0.030  |  0.653 | 0.211 |

## 2nd run
| Operation                    | Postgres | MS SQL | Oracle | MySQL  | MariaDB | Cockroach |
| ---                    | --- | --- | --- | ---  | ---  | ---  |
| Researcher to Paper          | 0.005    | 0.004  | 0.024  | 0.003  |  0.002 | 0.022 |
| Researcher to Topic          | 0.005    | 0.003  | 0.017  | 0.003  |  0.003 | 0.043 |
| Researcher to Conference     | 0.009    | 0.003  | 0.027  | 0.003  |  0.003 | 0.189 |
| Researcher to Organization   | 0.020    | 0.004  | 0.018  | 0.004  |  0.004 | 0.203 |

## NoSQL
| Operation                    | MongoDB | Redis |  |   |  |  |
| ---                    |---------|-------| --- | ---  | ---  | ---  |
| Researcher to Paper          | 20.93   | 1.13  |   |   |   |  |
| Researcher to Topic          | 30.63   | 1.12  |   |   |   |  |
| Researcher to Conference     | 34.97   | 1.11  |   |   |   |  |
| Researcher to Organization   | 38.30   | 1.12  |   |   |   |  |
