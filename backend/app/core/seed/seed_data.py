from app.core.database.postgresql import async_session_maker
from app.services.category_service import CategoryService
from app.services.size_service import SizeService
from app.services.product_service import ProductService
from app.schemas.category import CategoryCreate
from app.schemas.size import SizeCreate, SizeUpdate
from app.schemas.product import ProductCreate, ProductSizeAdd


async def seed_categories():
    async with async_session_maker() as db:
        try:
            category_service = CategoryService(db)

            existing_categories = await category_service.get_all_categories()
            if len(existing_categories) > 0:
                return

            categories = [
                CategoryCreate(name="Electronics"),
                CategoryCreate(name="Clothing"),
                CategoryCreate(name="Books"),
                CategoryCreate(name="Sports"),
                CategoryCreate(name="Home")
            ]

            for category in categories:
                await category_service.create_category(category)

        except Exception as e:
            print(f"Seed categories error: {e}")


async def seed_sizes():
    async with async_session_maker() as db:
        try:
            size_service = SizeService(db)

            existing_sizes = await size_service.get_sizes()
            if len(existing_sizes) > 0:
                return

            sizes = [
                SizeCreate(name="XS"),
                SizeCreate(name="S"),
                SizeCreate(name="M"),
                SizeCreate(name="L"),
                SizeCreate(name="XL"),
                SizeCreate(name="XXL"),
                SizeCreate(name="Black"),
                SizeCreate(name="Orange"),
            ]

            for idx, size in enumerate(sizes):
                try:
                    created_size = await size_service.create_size(size)
                    await size_service.update_size(created_size.id, SizeUpdate(display_order=idx + 1))
                except Exception as inner_e:
                    print(f"Error creating size {size.name}: {inner_e}")
                    import traceback
                    traceback.print_exc()

        except Exception as e:
            print(f"Seed sizes error: {e}")
            import traceback
            traceback.print_exc()


async def seed_products():
    async with async_session_maker() as db:
        try:
            product_service = ProductService(db)
            category_service = CategoryService(db)
            size_service = SizeService(db)

            existing_products = await product_service.get_products()
            if len(existing_products) > 0:
                return

            categories = await category_service.get_all_categories()
            if len(categories) == 0:
                return

            sizes = await size_service.get_sizes()
            if len(sizes) == 0:
                return

            category_map = {cat.name: cat.id for cat in categories}
            size_map = {size.name: size.id for size in sizes}

            products_data = [
                {
                    "product": ProductCreate(
                        name="Headphone",
                        description="High quality wireless headphones",
                        category_id=category_map.get("Electronics", 1)
                    ),
                    "sizes": [
                        ProductSizeAdd(size_id=size_map.get("Black", 1), price=200, stock=50),
                        ProductSizeAdd(size_id=size_map.get("Orange", 1), price=200, stock=50),
                    ]
                },
                {
                    "product": ProductCreate(
                        name="Smart Watch",
                        description="Heart rate monitor smart watch",
                        category_id=category_map.get("Electronics", 1)
                    ),
                    "sizes": [
                        ProductSizeAdd(size_id=size_map.get("Black", 1), price=300, stock=30),
                        ProductSizeAdd(size_id=size_map.get("Orange", 1), price=300, stock=45),
                    ]
                },
                {
                    "product": ProductCreate(
                        name="T-Shirt",
                        description="Cotton comfortable t-shirt",
                        category_id=category_map.get("Clothing", 2)
                    ),
                    "sizes": [
                        ProductSizeAdd(size_id=size_map.get("S", 1), price=40, stock=100),
                        ProductSizeAdd(size_id=size_map.get("M", 1), price=40, stock=120),
                        ProductSizeAdd(size_id=size_map.get("L", 1), price=40, stock=90),
                        ProductSizeAdd(size_id=size_map.get("XL", 1), price=40, stock=60),
                    ]
                },
                {
                    "product": ProductCreate(
                        name="Running Shoes",
                        description="Lightweight running shoes",
                        category_id=category_map.get("Sports", 4)
                    ),
                    "sizes": [
                        ProductSizeAdd(size_id=size_map.get("M", 1), price=50, stock=40),
                        ProductSizeAdd(size_id=size_map.get("L", 1), price=50, stock=50),
                        ProductSizeAdd(size_id=size_map.get("XL", 1), price=50, stock=35),
                    ]
                },
                {
                    "product": ProductCreate(
                        name="Programming Book",
                        description="Complete guide to programming for beginners",
                        category_id=category_map.get("Books", 3)
                    ),
                    "sizes": [
                        ProductSizeAdd(size_id=size_map.get("M", 1), price=55, stock=200),
                    ]
                },
                {
                    "product": ProductCreate(
                        name="Coffee Maker",
                        description="Coffee maker for home use",
                        category_id=category_map.get("Home", 5)
                    ),
                    "sizes": [
                        ProductSizeAdd(size_id=size_map.get("M", 1), price=84, stock=25),
                    ]
                },
                {
                    "product": ProductCreate(
                        name="Yoga Mat",
                        description="Yoga mat for home use",
                        category_id=category_map.get("Sports", 4)
                    ),
                    "sizes": [
                        ProductSizeAdd(size_id=size_map.get("M", 1), price=33, stock=80),
                    ]
                },
                {
                    "product": ProductCreate(
                        name="Jeans",
                        description="Jeans for home use",
                        category_id=category_map.get("Clothing", 2)
                    ),
                    "sizes": [
                        ProductSizeAdd(size_id=size_map.get("S", 1), price=66, stock=60),
                        ProductSizeAdd(size_id=size_map.get("M", 1), price=66, stock=75),
                        ProductSizeAdd(size_id=size_map.get("L", 1), price=66, stock=70),
                        ProductSizeAdd(size_id=size_map.get("XL", 1), price=66, stock=50),
                        ProductSizeAdd(size_id=size_map.get("XXL", 1), price=66, stock=40),
                    ]
                }
            ]

            for item in products_data:
                created_product = await product_service.create_product(item["product"])
                for size_data in item["sizes"]:
                    await product_service.add_size_to_product(created_product.id, size_data)

        except Exception as e:
            print(f"Seed products error: {e}")


async def seed_all_data():
    await seed_categories()
    await seed_sizes()
    await seed_products()
