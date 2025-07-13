import os
import duckdb
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from app.db import db_path
from app.db.setup import engine
print(db_path)

engine.dispose()
load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
table_name = 'detail'
embeddings_table_name = 'details_embedding'
model_size = 3072

"Project: Mayhemimmerses you into an electrifying multiplayer PvP showdown, fueled entirely by explosive grenade-based combat. Enter dynamic, futuristic arenas and master the art of projectile trajectory, precise timing, and interactive environments to tactically outmaneuver and overpower rival teams.Explosive PvP ActionDive into adrenaline-pumping team deathmatches where every throw counts. Strategically lob grenades, predict enemy movements, and create spectacular chain reactions to secure victory in intense, high-stakes battles.Dynamic Sci-Fi ArenasNavigate and dominate futuristic battlegrounds designed to elevate combat. Use teleportation portals to flank foes, bounce pads for rapid repositioning, and engage with interactive hazards to turn the environment into your ally.Customizable LoadoutsTailor your playstyle with an extensive arsenal. Choose from a variety of grenades—ranging from incendiary and gravity-defying options to scatter types—supplemented by deployable drones, defensive barriers, and mobility abilities such as agile dashes and evasive rolls.Fluid Movement & Vertical TacticsTraverse across obstacles and mantle boxes to gain the upper hand. Surprise enemies from unexpected angles, using verticality and environmental navigation to outsmart and outmaneuver your opponents.Friendly Fire FrenzyPrecision and chaos collide as every explosion threatens friends and foes alike. Coordinate carefully with teammates while managing explosive risks, pushing your strategic thinking and reflexes to their limits.Gear up, strategize closely with your squad, and brace yourself—it's time to unleash total mayhem!"

with duckdb.connect(db_path) as conn:
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {embeddings_table_name} (
            id VARCHAR,
            name VARCHAR,
            text TEXT,
            embedding FLOAT[{model_size}]
        );
    """)
    conn.execute("INSTALL vss;")
    conn.execute("LOAD vss;")
    conn.execute("SET hnsw_enable_experimental_persistence = true;")
    conn.execute(f"""
    CREATE INDEX IF NOT EXISTS description_index ON {embeddings_table_name} USING HNSW (embedding)
    """)
    df = conn.execute(
        f"""
    SELECT
        id,
        name,
        SUBSTR(
            CONCAT(
                short_description,
                '\n\n',
                detailed_description,
                '\n\n',
                about_the_game
            ),
            1,
            60000
        ) AS text
    FROM detail
    WHERE CAST(id AS VARCHAR) not in (
        SELECT id from {embeddings_table_name}
    )
        """
    ).df()
    print(df)
    df['embedding'] = embeddings.embed_documents(df['text'].tolist(), chunk_size=200)
    df = df[['id', 'name', 'text', 'embedding']]
    conn.execute(f"INSERT INTO {embeddings_table_name} SELECT * FROM df;")
    query = 'quero um jogo de mayhem bem doidao'
    query_embedding = embeddings.embed_query(query)
    results = conn.execute(
        f"""
SELECT name, text
FROM {embeddings_table_name}
ORDER BY array_distance(embedding, array{query_embedding}::FLOAT[{model_size}])
LIMIT 3
        """
    ).df()


    print(results)


