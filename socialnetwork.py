from neo4j import GraphDatabase
class SocialNetworkApp:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        try:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
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

    #UC-5: Follow Another User
    def follow_user(self, follower, followee):
        query = """
        placeholder
        """
        self.execute_query(query, {"follower": follower, "followee": followee})
        print(f"{follower} now follows {followee}!")

    #UC-6: Unfollow a User
    def unfollow_user(self, follower, followee):
        query = """
        placeholder
        """
        self.execute_query(query, {"follower": follower, "followee": followee})
        print(f"{follower} has unfollowed {followee}.")

    #UC-7: View Friends/Connections
    def view_following(self, user):
        query = """
        placeholder
        """
        following = self.execute_query(query, {"user": user})
        if following:
            print(f"{user} is following: {[f['following'] for f in following]}")
        else:
            print(f"{user} is not following anyone.")

    def view_followers(self, user):
        query = """
        placeholder
        """
        followers = self.execute_query(query, {"user": user})
        if followers:
            print(f"{user} has followers: {[f['follower'] for f in followers]}")
        else:
            print(f"{user} has no followers.")

    #UC-8: Mutual Connections
    def mutual_connections(self, user1, user2):
        query = """
        placeholder
        """
        mutual_friends = self.execute_query(query, {"user1": user1, "user2": user2})
        if mutual_friends:
            print(f"Mutual connections between {user1} and {user2}: {[f['mutualFriend'] for f in mutual_friends]}")
        else:
            print(f"{user1} and {user2} have no mutual connections.")
