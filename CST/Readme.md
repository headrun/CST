# CST

**Url: /cst/admin/**

### Flow
    1. Add Client. (Skip if already present)
    2. Add Project(s) for a particular client. (Skip if already present)
    3. Add Crawler(s) for different projects.

### Processes to Add/Edit Things
**Prequisite:** You Must a Super user o do this

    1. Adding a crawling team developer:
        1.1 Create/Add user in Authentication/Users.
        1.2 Change prmission and mark staff member (NOT super user status).
        1.3 Add User to group in same page to 'Crawler_developers'.
------
**Prequisite:** You Must be part of 'Crawler_developers' django group

    2. Adding/Editing a Crawler:
        2.1 Login into admin Dashboard.
        2.2 Navigate to Crawlers.
        2.3 Add/Edit Crawler with all the requird fields.
------

**Prequisite:** You Must a Super user o do this

    3. Adding a Client:
        3.1 Login into Admin dashboard.
        3.2 Navigate to Projects then Clients.
        3.3 Add/Edit the Client.
------

**Prequisite:** You Must a Super user o do this

    4. Adding a Project for a client:
        3.1 Login into Admin dashboard.
        3.2 Navigate to Projects then Projects.
        3.3 Add/Edit the Projects.
------
