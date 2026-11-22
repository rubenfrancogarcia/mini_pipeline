from DBUtils import DBUtils

class CLIService:
    def __init__(self):
        db = DBUtils()
        self.menu = {
            "1": ("Top 3 events by tickets sold", db.find_by_most_tickets),
            "2": ("Revenue by city", db.revenue_by_city),
            "3": ("Tickets for a customer", db.tickets_for_customer),
            "4": ("Least popular 3 events by tickets sold", db.find_by_least_tickets),
            "5": ("Return all results", db.return_all_results),
        }

    def run_menu(self, connection):
        while True:
            print()
            print("Options")
            for key, (label, _) in self.menu.items():
                print(f" {key}. {label}")
            print(" q. Quit")

            choice = input("> ").strip().lower()
            if choice == "q":
                break
            if choice not in self.menu:
                print("Invalid choice")
                continue
            _, action = self.menu[choice]
            action(connection)
