def main():
    while True:
        print("\n--- Social Network ---")
        print("1. Register")
        print("2. Follow User")
        print("3. View Followers")
        print("4. View Following")
        print("5. Recommend Users")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter new username: ")
            print(f"User '{username}' registered!")

        elif choice == "2":
            follower = input("Enter your username: ")
            followee = input("Enter user to follow: ")
            print(f"'{follower}' now follows '{followee}'")

        elif choice == "3":
            user = input("Enter username to check followers: ")
            print(f"Followers of {user}: ")

        elif choice == "4":
            user = input("Enter username to check following: ")
            print(f"{user} is following: ")

        elif choice == "5":
            user = input("Enter username to get recommendations: ")
            print(f"Recommended connections for {user}: ")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()