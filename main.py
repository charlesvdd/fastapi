- # Récupération des variables d’environnement
- DB_USER     = os.getenv("POSTGRES_USER")
- DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
- DB_HOST     = os.getenv("DB_HOST")
- DB_NAME     = os.getenv("POSTGRES_DB")
- DB_PORT     = os.getenv("DB_PORT", "5432")
+ # Récupération des variables d’environnement
+ DB_USER     = os.getenv("POSTGRES_USER")
+ DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
+ DB_HOST     = os.getenv("DB_HOST")        # seulement si défini
+ DB_NAME     = os.getenv("POSTGRES_DB")
+ DB_PORT     = os.getenv("DB_PORT", "5432")

 @app.on_event("startup")
 async def startup():
-    try:
-        app.state.db = await asyncpg.create_pool(
-            user=DB_USER,
-            password=DB_PASSWORD,
-            host=DB_HOST,
-            port=int(DB_PORT),
-            database=DB_NAME,
-        )
-    except Exception as e:
-        print(f"[ERROR] Cannot connect to database: {e}")
-        raise
+    # Ne tente la connexion que si un host est configuré
+    if DB_HOST:
+        try:
+            app.state.db = await asyncpg.create_pool(
+                user=DB_USER,
+                password=DB_PASSWORD,
+                host=DB_HOST,
+                port=int(DB_PORT),
+                database=DB_NAME,
+            )
+        except Exception as e:
+            print(f"[ERROR] Cannot connect to database: {e}")
+            # On ne lève plus pour ne pas bloquer le démarrage
+            app.state.db = None
+    else:
+        print("[INFO] DB_HOST not set – skipping database connection")

 @app.on_event("shutdown")
 async def shutdown():
-    await app.state.db.close()
+    if getattr(app.state, "db", None):
+        await app.state.db.close()
