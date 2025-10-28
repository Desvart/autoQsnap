| Entity            | Attribute                          | Data Type            | Description                                                      |  
|-------------------|------------------------------------|----------------------|------------------------------------------------------------------|
|                   |                                    |                      |                                                                  |
| Data              | data_id                            | INT                  | (PK) Unique identifier for each data                             |
|                   | creation_date                      | DATE                 | Date when object has been created                                |
|                   | type                               | VARCHAR(255)         | Type of the data (enum)                                          |
|                   | value                              | ?                    |                                                                  |
|                   | Sources                            | {Data, VARCHAR(255)} |                                                                  |
|                   |                                    |                      |                                                                  |
| Metric            | metric_id                          | INT                  | (PK)                                                             |
|                   | description                        | TEXT                 |                                                                  |
|                   | formula                            | TEXT                 |                                                                  |
|                   | approximate                        | TEXT                 | Description of the underlying intention for such metric to exist |
|                   |                                    |                      |                                                                  |
| User_satisfaction |                                    |                      |                                                                  |
|                   |                                    |                      |                                                                  |
| Snapshot          |                                    |                      |                                                                  |
|                   |                                    |                      |                                                                  |
| Application       | application_id                     | INT                  | (PK)                                                             |
|                   | creation_date                      | DATE                 |                                                                  |
|                   | trigram                            | VARCHAR(3)           |                                                                  |
|                   | name                               | VARCHAR(255)         |                                                                  |
|                   | eacode                             | VARCHAR(10)          |                                                                  |
|                   | crown_jewels_level                 | VARCHAR(5)           |                                                                  |
|                   | priority_level                     | VARCHAR(2)           |                                                                  |
|                   | enterprise_service                 | BOOL                 |                                                                  |
|                   | web_exposure                       | BOOL                 |                                                                  |
|                   | make_or_buy                        | VARCHAR(10)          |                                                                  |
|                   | product_owner                      | VARCHAR(255)         |                                                                  |
|                   | product_manager                    | VARCHAR(255)         |                                                                  |
|                   | flagged_for_deletion               | BOOL                 |                                                                  |
|                   | wiki_main_url                      | VARCHAR(255)         |                                                                  |
|                   | jira_main_url                      | VARCHAR(255)         |                                                                  |
|                   | git_main_urls                      | VARCHAR(255)         |                                                                  |
|                   | sonar_main_urls                    | VARCHAR(255)         |                                                                  |
|                   | domain                             | VARCHAR(255)         |                                                                  |
|                   | platform                           | VARCHAR(255)         |                                                                  |
|                   |                                    |                      |                                                                  |
| Incident          | incident_id                        | INT                  | (PK)                                                             |
|                   | creation_date                      | DATE                 |                                                                  |
|                   | jira_id                            | VARCHAR(10)          |                                                                  |
|                   | incident_creation_date             | DATE                 |                                                                  |
|                   | resolution_date                    | DATE                 |                                                                  |
|                   | priority                           | VARCHAR(10)          |                                                                  |
|                   | resolution_category                | VARCHAR(255)         |                                                                  |
|                   | financial_impact                   | INT                  |                                                                  |
|                   | faulty_application                 | INT                  | (FK)                                                             |
|                   | reporter                           | VARCHAR(255)         |                                                                  |
|                   | assignee                           | VARCHAR(255)         |                                                                  |
|                   | impacted_application               | {INT}                | (FK)                                                             |
|                   | flagged_as_not_an_incident         | BOOL                 |                                                                  |
|                   |                                    |                      |                                                                  |
| Problem           | problem_id                         | INT                  | (PK)                                                             |
|                   | creation_date                      | DATE                 |                                                                  |
|                   | jira_id                            | VARCHAR(10)          |                                                                  |
|                   | problem_creation_date              | DATE                 |                                                                  |
|                   | resolution_date                    | DATE                 |                                                                  |
|                   | priority                           | VARCHAR(10)          |                                                                  |
|                   | reporter                           | VARCHAR(255)         |                                                                  |
|                   | assignee                           | VARCHAR(255)         |                                                                  |
|                   | impacted_application               | {INT}                | (FK)                                                             |
|                   |                                    |                      |                                                                  |
| Release           | release_id                         | INT                  | (PK)                                                             |
|                   | creation_date                      | DATE                 |                                                                  |
|                   | application_id                     | INT                  | (FK)                                                             | 
|                   | version_number                     | VARCHAR(255)         |                                                                  |
|                   | release_date                       | DATE                 |                                                                  |
|                   | scope                              | TEXT                 |                                                                  |
|                   | change_request_id                  | VARCHAR(10)          |                                                                  |
|                   |                                    |                      |                                                                  |
| Static_quality    | static_quality_id                  | INT                  | (PK)                                                             |
|                   | creation_date                      | DATE                 |                                                                  |
|                   | application_id                     | INT                  | (FK)                                                             |
|                   | maintainability_score              | VARCHAR(1)           |                                                                  |
|                   | reliability_score                  | VARCHAR(1)           |                                                                  |
|                   | security_score                     | VARCHAR(1)           |                                                                  |
|                   | security_review_score              | VARCHAR(1)           |                                                                  |
|                   | coverage                           | INT                  |                                                                  |
|                   | gate_level                         | VARCHAR(255)         |                                                                  |
|                   | branch                             | VARCHAR(255)         |                                                                  |
|                   | repository                         | VARCHAR(255)         |                                                                  |
|                   | number_of_lines                    | INT                  |                                                                  |
|                   |                                    |                      |                                                                  |
| Interviews        | interview_id                       | INT                  | (PK)                                                             |
|                   | creation_date                      | DATE                 |                                                                  |
|                   | application_id                     | INT                  | (FK)                                                             |
|                   | functional_statisfaction_score     | INT                  |                                                                  |
|                   | non_functional_statisfaction_score | INT                  |                                                                  |
|                   | feature_map                        | VARCHAR(10)          |                                                                  |
|                   | dependency_diagram                 | VARCHAR(10)          |                                                                  |
|                   | consumer_list                      | VARCHAR(10)          |                                                                  |
|                   | inflow_data_quality_control        | VARCHAR(10)          |                                                                  |
|                   | outflow_data_quality_control       | VARCHAR(10)          |                                                                  |
|                   | incidents_on_data_quality          | VARCHAR(10)          |                                                                  |
|                   | test_strategy                      | VARCHAR(10)          |                                                                  |
|                   | rcsa_matrix                        | VARCHAR(10)          |                                                                  |
|                   | risk_analysis                      | VARCHAR(10)          |                                                                  |
|                   | formal_test_campaigns              | VARCHAR(10)          |                                                                  |
|                   | functional_acceptance_tests        | VARCHAR(10)          |                                                                  |
|                   | fat_regression                     | VARCHAR(10)          |                                                                  |
|                   | scripted_tests                     | VARCHAR(10)          |                                                                  |
|                   | test_contracts                     | VARCHAR(10)          |                                                                  |
|                   | load_tests                         | VARCHAR(10)          |                                                                  |
|                   | user_acceptance_tests              | VARCHAR(10)          |                                                                  |
|                   | uat_regression                     | VARCHAR(10)          |                                                                  |
|                   | uat_business_testers               | VARCHAR(10)          |                                                                  |
|                   | automated_regression               | VARCHAR(10)          |                                                                  |
|                   | automated_contract_first           | VARCHAR(10)          |                                                                  |
|                   | automated_contract_tests           | VARCHAR(10)          |                                                                  |