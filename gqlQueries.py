from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Initialize GraphQL variables
transport = AIOHTTPTransport(url="https://hub.snapshot.org/graphql", headers={'Content-Type': 'application/json'})
gqlclient = Client(transport=transport, fetch_schema_from_transport=True)

#Snapshot query blocks, for active and closed proposals
async def snapshotQuery(space):
    query = gql(
        """
        query Proposals ($space_in: String!) {
                proposals(
                    where: {
                    space_in: [$space_in],
                    state: "active"
                    },
                    orderBy: "created",
                    orderDirection: desc
                ) {
                    id
                    title
                    body
                    choices
                    start
                    end
                    snapshot
                    scores
                    scores_total
                    quorum
                    author
                }
                }
            """
        )
    params = {"space_in": space}
    result = await gqlclient.execute_async(query, variable_values=params)
    return result

async def snapshotClosedQuery(space):
    query = gql(
        """
        query Proposals ($space_in: String!) {
                proposals(
                    where: {
                    space_in: [$space_in],
                    state: "closed"
                    },
                    orderBy: "created",
                    orderDirection: desc
                ) {
                    id
                    title
                    body
                    choices
                    start
                    end
                    snapshot
                    scores
                    scores_total
                    author
                }
                }
            """
        )
    params = {"space_in": space}
    result = await gqlclient.execute_async(query, variable_values=params)
    return result