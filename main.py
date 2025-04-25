from socialnetwork import SocialNetworkApp

def main():
    app = SocialNetworkApp("bolt://localhost:7687", "neo4j", "password")
    while True:
        print("\n--- Social Network ---")
        print("1. Register User")
        print("2. Login")
        print("3. View Profile")
        print("4. Edit Profile")
        print("5. Follow User")
        print("6. Unfollow User")
        print("7. View Connections")
        print("8. Mutual Connections")
        print("9. Recommend Friends")
        print("10. Search Users")
        print("11. Explore Popular Users")
        print("12. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            name = input("Enter name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            app.register_user(username, name, email, password)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            app.login_user(username, password)

        elif choice == "3":
            username = input("Enter username: ")
            app.view_profile(username)

        elif choice == "4":
            username = input("Enter username: ")
            name = input("Enter new name (leave blank to keep current): ")
            bio = input("Enter new bio (leave blank to keep current): ")
            app.edit_profile(username, name, bio)

        elif choice == "5":
            follower = input("Enter your username: ")
            followee = input("Enter username to follow: ")
            app.follow_user(follower, followee)

        elif choice == "6":
            follower = input("Enter your username: ")
            followee = input("Enter username to unfollow: ")
            app.unfollow_user(follower, followee)

        elif choice == "7":
            username = input("Enter your username: ")
            app.view_connections(username)

        elif choice == "8":
            user1 = input("Enter first username: ")
            user2 = input("Enter second username: ")
            app.mutual_connections(user1, user2)

        elif choice == "9":
            username = input("Enter your username: ")
            app.recommend_friends(username)

        elif choice == "10":
            name = input("Enter name or username to search: ")
            app.search_users(name)

        elif choice == "11":
            app.explore_popular_users()

        elif choice == "12":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()