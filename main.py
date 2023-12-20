import datetime
import json

import application
import server


def main() -> None:
    application_instance: application.Application = application.Application()
    server_instance: server.Server = server.Server(application_instance)
    server_instance.start()

    while True:
        command = input("> ")
        match command.split(" ")[0].upper():
            case "QUIT":
                server_instance.stop()
                break
            case "RESTART":
                application_instance = application.Application()
                server_instance.replace_application(application_instance)
            case "REFILL":
                for resource in application_instance.ship.data["resources"]:
                    application_instance.ship.data["resources"][resource]["amount"].set(
                        application_instance.ship.data["resources"][resource]["maxAmount"].get()
                    )
                application_instance.ship.validate_abilities()
            case "SAVE":
                with open("saveFile.json", "w") as file:
                    file.write(json.dumps(application_instance.ship.data.get_updated(datetime.datetime(1, 1, 1))))


if __name__ == '__main__':
    main()
