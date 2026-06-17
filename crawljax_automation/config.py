APPS = [
        {
        "name": "addressbook",
        "url": "http://localhost:8090",
        "docker_path": "./apps/addressbook",
        "username": "test@test.com",
        "password": "Testing0099",

        "container_name": "addressbook-addressbook-1",
        "coverage_file":
            "/var/www/html/coverage/addressbook_coverage.ser",
        "coverage_export":
            "/var/www/html/export_coverage.php"
    },
    {
        "name": "ppma",
        "url": "http://localhost:8080",
        "docker_path": "./apps/ppma",
        "username": "test",
        "password": "Test0099",

        "container_name": "ppma-ppma-1",
        "coverage_file":
            "/var/www/html/coverage/ppma_coverage.ser",
        "coverage_export":
            "/var/www/html/export_coverage.php"
    }
]

SAS_LIST = [
    "basic",
    "dhash",
    "functionality_extraction"
]