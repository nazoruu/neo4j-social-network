from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError


class SocialNetworkApp:
    def __init__(self, uri, user, password):
        self._authenticated = None
        self._uri = uri
        self._user = user
        self._password = password
        try:
            self._driver = GraphDatabase.driver(
                self._uri, auth=(self._user, self._password)
            )
            self._check_connection()
            print("Connected to Neo4j successfully!")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")

    def _check_connection(self):
        with self._driver.session() as session:
            session.run("RETURN 1")

    def close(self):
        self._driver.close()

    def execute_query(self, query, parameters=None):
        with self._driver.session() as session:
            return session.execute_write(self._run_query, query, parameters)

    @staticmethod
    def _run_query(tx, query, parameters=None):
        result = tx.run(query, parameters)
        return [record for record in result]

    # UC-1: Register User
    def register_user(self, username, name, email, password):
        print("OUPUT--------------------------------------------")
        try:
            check_query = """
                CREATE (:Person {
                    email: $email,
                    username: $username,
                    name: $name,
                    password: $password
                })
            """
            self.execute_query(
                check_query,
                {
                    "email": email,
                    "username": username,
                    "name": name,
                    "password": password,
                },
            )
            print(
                f"User {username} registered with name {name} and email {email}"
            )
            self._authenticated = username
            return True
        except ConstraintError:
            print("Email and username must be unique")
            return False

    # UC-2: User Login
    def login_user(self, email, password):
        print("OUPUT--------------------------------------------")
        check_query = """
            MATCH (p:Person {email: $email, password: $password})
            RETURN p LIMIT 1
        """
        result = self.execute_query(check_query, {"email": email, "password": password})

        if len(result) > 0:
            user = result[0]["p"]
            self._authenticated = user["username"]
            print(f"User {user['email']} logged in")
        else:
            print("Invalid email or password")

    def logout(self):
        print("OUPUT--------------------------------------------")
        self._authenticated = None
        print("Logged out")

    # UC-3: View Profile
    def view_profile(self):
        print("OUPUT--------------------------------------------")
        if not self._authenticated:
            print("Authentication required")
            return

        result = self.execute_query("""
                MATCH (p:Person {username: $username})
                RETURN p.name AS name, p.username AS username, p.email AS email, p.password AS password
                LIMIT 1
            """, {"username": self._authenticated})

        record = result[0] if len(result) > 0 else None
        if record:
            print("User Profile:")
            print("Email:", record["email"])
            print("Username:", record["username"])
            print("Name:", record["name"])
        else:
            print("User does not exist.")

    # UC-4: Edit Profile
    def edit_profile(self, name, password):
        print("OUPUT--------------------------------------------")
        if not self._authenticated:
            print("Authentication required")
            return

        result = self.execute_query(
            """
            MATCH (p:Person {username: $username})
            RETURN p
            LIMIT 1
        """,
            {"username": self._authenticated},
        )

        if len(result) == 0:
            print("User does not exist.")
            return

        set_clauses = []
        params = {"username": self._authenticated}

        if name != "":
            set_clauses.append("p.name = $name")
            params["name"] = name
        if password != "":
            set_clauses.append("p.password = $password")
            params["password"] = password

        if not set_clauses:
            print("No updates requested.")
            return

        set_query = ", ".join(set_clauses)

        # Execute update query
        result = self.execute_query(
            f"""
            MATCH (p:Person {{username: $username}})
            SET {set_query}
            RETURN p.name AS name, p.username AS username, p.email AS email, p.password AS password
        """,
            params,
        )

        updated_user = result[0] if len(result) > 0 else None
        if updated_user:
            print("User updated successfully.")
            print("Updated Profile:")
            print("Name:", updated_user["name"])
            print("Username:", updated_user["username"])
            print("Email:", updated_user["email"])
            print("Password:", updated_user["password"])
        else:
            print("Unexpected error: User not found after update.")

    # UC-5: Follow Another User
    def follow_user(self, followee):
        print("OUPUT--------------------------------------------")
        if not self._authenticated:
            print("Authentication required")
            return

        # First check if relationship exists
        check_query = """
        MATCH (a:Person {username: $follower})-[r:FOLLOWS]->(b:Person {username: $followee})
        RETURN COUNT(r) AS relCount
        """
        result = self.execute_query(
            check_query, {"follower": self._authenticated, "followee": followee}
        )

        if result and result[0]["relCount"] > 0:
            print(f"{self._authenticated} already follows {followee}.")
        else:
            follow_query = """
            MATCH (a:Person {username: $follower}), (b:Person {username: $followee})
            MERGE (a)-[:FOLLOWS]->(b)
            """
            self.execute_query(
                follow_query, {"follower": self._authenticated, "followee": followee}
            )
            print(f"{self._authenticated} now follows {followee}!")

    # UC-6: Unfollow a User
    def unfollow_user(self, followee):
        print("OUPUT--------------------------------------------")
        if not self._authenticated:
            print("Authentication required")
            return

        # First check if relationship exists
        check_query = """
        MATCH (a:Person {username: $follower})-[r:FOLLOWS]->(b:Person {username: $followee})
        RETURN COUNT(r) AS relCount
        """
        result = self.execute_query(
            check_query, {"follower": self._authenticated, "followee": followee}
        )

        if result and result[0]["relCount"] == 0:
            print(f"{self._authenticated} is not following {followee}.")
        else:
            unfollow_query = """
            MATCH (a:Person {username: $follower})-[r:FOLLOWS]->(b:Person {username: $followee})
            DELETE r
            """
            self.execute_query(
                unfollow_query, {"follower": self._authenticated, "followee": followee}
            )
            print(f"{self._authenticated} has unfollowed {followee}.")

    # UC-7: View Friends/Connections
    def view_following(self):
        print("OUPUT--------------------------------------------")
        if not self._authenticated:
            print("Authentication required")
            return

        query = """
        MATCH (:Person {username: $username})-[:FOLLOWS]->(f:Person)
        RETURN f.name AS following
        """
        following = self.execute_query(query, {"username": self._authenticated})
        if following:
            print(f"{self._authenticated} is following: {[f['following'] for f in following]}")
        else:
            print(f"{self._authenticated} is not following anyone.")

    def view_followers(self):
        print("OUPUT--------------------------------------------")
        if not self._authenticated:
            print("Authentication required")
            return

        query = """
        MATCH (f:Person)-[:FOLLOWS]->(:Person {username: $username})
        RETURN f.name AS follower
        """
        followers = self.execute_query(query, {"username": self._authenticated})
        if followers:
            print(f"{self._authenticated} has followers: {[f['follower'] for f in followers]}")
        else:
            print(f"{self._authenticated} has no followers.")

    # UC-8: Mutual Connections
    def mutual_connections(self, user):
        print("OUPUT--------------------------------------------")
        if not self._authenticated:
            print("Authentication required")
            return

        query = """
        MATCH (a:Person {username: $user1})-[:FOLLOWS]->(m:Person)<-[:FOLLOWS]-(b:Person {username: $user2})
        RETURN m.username AS mutualFriend
        """
        mutual_friends = self.execute_query(query, {"user1": self._authenticated, "user2": user})
        if mutual_friends:
            print(
                f"Mutual connections between {self._authenticated} and {user}: {[f['mutualFriend'] for f in mutual_friends]}"
            )
        else:
            print(f"{self._authenticated} and {user} have no mutual connections.")

    # UC-9: Friend Recommendations
    def recommend_friends(self):
        print("OUPUT--------------------------------------------")
        if not self._authenticated:
            print("Authentication required")
            return

        query = """
        MATCH (a:Person {name: $username})-[:FOLLOWS]->(b:Person)-[:FOLLOWS]->(c:Person)
        WHERE NOT (a)-[:FOLLOWS]->(c) AND a <> c
        RETURN DISTINCT c.username AS recs
        """
        recs = self.execute_query(query, {"username": self._authenticated})
        recs_list = set([f['recs'] for f in recs])
        if len(recs_list) > 0:
            print(
                f"Possible people for {self._authenticated} to follow: {list(recs_list)}"
            )
        else:
            print(f"No follow suggestions for {self._authenticated} to follow.")

    # UC-10: Search Users
    def search_users(self, query):
        print("OUPUT--------------------------------------------")
        if query == "":
            print("Please enter a query to search for users.")
            return

        result = self.execute_query("""
            MATCH (p:Person)
            WHERE toLower(p.name) CONTAINS toLower($query)
               OR toLower(p.username) CONTAINS toLower($query)
            RETURN p.name AS name, p.username AS username, p.email AS email
            LIMIT 15
        """, {"query": query})

        if result:
            print("Search results (limited to 15):")
            for user in result:
                print(f"NAME: {user['name']}, USERNAME: {user['username']}, EMAIL: {user['email']}")
        else:
            print("No matching users found.")

    # UC-11: Explore popular users
    def explore_popular_users(self):
        print("OUPUT--------------------------------------------")
        result = self.execute_query("""
            MATCH (follower:Person)-[:FOLLOWS]->(person:Person)
            WITH person, COUNT(follower) AS followers
            WHERE followers > 0
            RETURN person.name AS name, person.username AS username, followers
            ORDER BY followers DESC
            LIMIT 15
        """)

        if result:
            print("Top followed users (limited to 15):")
            for user in result:
                print(f"NAME: {user['name']}, USERNAME: {user['username']}, FOLLOWER COUNT: {user['followers']}")
        else:
            print("No followed users found.")
