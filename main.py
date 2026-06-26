import socket
from datetime import datetime


COMMON_SERVICES = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    135: "RPC",
    137: "NetBIOS",
    138: "NetBIOS",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    179: "BGP",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    514: "Syslog",
    587: "SMTP Submission",
    636: "LDAPS",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP Alternate"
}


def scan_ports(host, start_port, end_port):
    results = []

    total_ports = end_port - start_port + 1

    print("\nScanning Started...")
    print(f"Target: {host}")
    print(f"Port Range: {start_port}-{end_port}\n")

    scanned = 0

    for port in range(start_port, end_port + 1):
        scanned += 1

        try:
            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(0.5)

            result = sock.connect_ex((host, port))

            if result == 0:
                service = COMMON_SERVICES.get(
                    port,
                    "Unknown Service"
                )

                results.append(
                    (port, "Open", service)
                )

                print(
                    f"Port {port} | Open | {service}"
                )

            sock.close()

        except Exception:
            pass

        progress = (scanned / total_ports) * 100

        print(
            f"\rProgress: {progress:.1f}%",
            end=""
        )

    print("\n\nScan Completed")

    return results


def export_results(results):
    if not results:
        print("No results available to export.")
        return

    filename = input(
        "\nEnter filename (without extension): "
    ).strip()

    if not filename:
        filename = "scan_results"

    filename += ".txt"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "Network Port Scanner Results\n"
        )

        file.write(
            f"Generated: {datetime.now()}\n\n"
        )

        for port, status, service in results:
            file.write(
                f"Port: {port} | "
                f"Status: {status} | "
                f"Service: {service}\n"
            )

    print(
        f"\nResults exported successfully to {filename}"
    )


def main():
    print("=" * 50)
    print("NETWORK PORT SCANNER")
    print("=" * 50)

    host = input(
        "Enter Host/IP Address: "
    ).strip()

    try:
        start_port = int(
            input("Enter Start Port: ")
        )

        end_port = int(
            input("Enter End Port: ")
        )

    except ValueError:
        print("Ports must be numeric.")
        return

    if start_port > end_port:
        print(
            "Start port cannot be greater than end port."
        )
        return

    results = scan_ports(
        host,
        start_port,
        end_port
    )

    if results:
        print("\nOpen Ports Found:\n")

        for port, status, service in results:
            print(
                f"{port:<10} {status:<10} {service}"
            )
    else:
        print(
            "\nNo open ports detected."
        )

    choice = input(
        "\nExport results? (y/n): "
    ).lower()

    if choice == "y":
        export_results(results)


if __name__ == "__main__":
    main()