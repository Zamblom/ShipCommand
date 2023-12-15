import typeguard

import application
import server


@typeguard.typechecked
def main():
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
                for resource in application_instance.ship.resources.values():
                    resource.refill()
                application_instance.ship.validate_abilities()


if __name__ == '__main__':
    main()
