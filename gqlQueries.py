from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import os
from dotenv import load_dotenv

load_dotenv()
DEFINEDAPI = os.getenv('DEFINED_API')


#Snapshot query blocks, for active and closed proposals. These utilized the api from snapshot.org, currently no api key is needed.
#Open votes
async def snapshotQuery(space):
    transport = AIOHTTPTransport(url="https://hub.snapshot.org/graphql", headers={'Content-Type': 'application/json'})
    gqlclient = Client(transport=transport, fetch_schema_from_transport=True)
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
                    votes
                }
                }
            """
        )
    params = {"space_in": space}
    result = await gqlclient.execute_async(query, variable_values=params)
    return result

#Closed votes
async def snapshotClosedQuery(space):
    transport = AIOHTTPTransport(url="https://hub.snapshot.org/graphql", headers={'Content-Type': 'application/json'})
    gqlclient = Client(transport=transport, fetch_schema_from_transport=True)
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
                    votes
                }
                }
            """
        )
    params = {"space_in": space}
    result = await gqlclient.execute_async(query, variable_values=params)
    return result

#Pull for contract data from Defined. address = contract address, poolIds is a list of IDs in the format ["1", "2", "3"].
#Example: contractData("0xECa9D81a4dC7119A40481CFF4e7E24DD0aaF56bD", ["16", "4", "7", "11", "19", "25", "30"])
#networkId is always 1 for now so this is hard coded
def contractData(address, poolIds):
    transport = AIOHTTPTransport(url="https://graph.defined.fi/graphql", headers={'content_type': 'application/json', 'Authorization': DEFINEDAPI})
    gqlclient = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql(
        """
        query getPrimePools($address: String!, $networkId: Int!, $poolIds: [String]){
            getPrimePools(address: $address, networkId: $networkId, poolIds: $poolIds) {
                items{
                    chainData {
                        primeAllocPoint
                    }
                    calcData {
                        sharePrimePerDay
                    }
                    totalSupply
                    poolId
                }
                }
            }
        """
    )
    params = {"address": address, "networkId": 1, "poolIds": poolIds}
    result = gqlclient.execute(query, variable_values=params)
    return result['getPrimePools']['items']