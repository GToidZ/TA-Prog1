import pytest
import skbin1  # import only skbin1 since it doesn't add any new functions in skbin2


class TestSKBinFunctions:
    def setup_method(self, method):
        self.menu = [
            "plain coffee",
            "caramel coffee",
            "brown sugar coffee",
            "latte",
            "caramel latte",
            "brown sugar latte",
            "plain tea",
            "brown sugar tea",
            "strawberry tea",
            "lychee tea",
            "milk tea",
            "caramel milk tea",
            "brown sugar milk tea",
            "plain milk",
            "caramel milk",
            "brown sugar milk",
            "strawberry milk",
        ]
        pass

    @pytest.mark.skip(reason="not a test")
    def get_syrup(self, drink: str):
        for idx, s in enumerate(["caramel", "brown sugar", "strawberry", "lychee"]):
            if s in drink:
                syrup_needed = [0, 0, 0, 0]
                syrup_needed[idx] += 10
                return s, syrup_needed
        return "", [0, 0, 0, 0]

    @pytest.mark.skip(reason="not a test")
    def get_base(self, drink: str, total: int):
        for s in ["milk tea", "coffee", "tea", "milk", "latte"]:
            if s in drink:
                base_needed = [0, 0, 0]
                if "latte" in s:
                    base_needed[0] += int(total / 2)
                    base_needed[2] += int(total / 2)
                elif "milk tea" in s:
                    base_needed[1] += int(total / 2)
                    base_needed[2] += int(total / 2)
                elif "coffee" in s:
                    base_needed[0] += total
                elif "tea" in s:
                    base_needed[1] += total
                else:
                    base_needed[2] += total
                return s, base_needed
        return "", [0, 0, 0]

    def test_all_functions_are_written(self, subtests):
        for func in ["get_ingredients", "check_stock", "update_stock", "get_price"]:
            with subtests.test(func=func):
                assert func in dir(skbin1), f"{func} does not exists"

    def test_get_price(self, subtests):
        for drink in self.menu:
            with subtests.test(drink=drink):
                price = 0
                if any(
                    [
                        (x in drink)
                        for x in ["caramel", "brown sugar", "strawberry", "lychee"]
                    ]
                ):
                    price += 5
                if any([(x in drink) for x in ["latte", "milk tea"]]):
                    price += 35
                else:
                    price += 25
                assert price == skbin1.get_price(
                    drink
                ), "price is not correctly computed"

    def test_get_ingredients(self, subtests):
        for drink in self.menu:
            with subtests.test(drink=drink):
                total = 30
                if any(
                    [
                        (x in drink)
                        for x in ["caramel", "brown sugar", "strawberry", "lychee"]
                    ]
                ):
                    amount = 10
                    total -= amount
                _, needed_syrup = self.get_syrup(drink)
                _, needed_base = self.get_base(drink, total)
                assert skbin1.get_ingredients(drink) == (needed_base, needed_syrup)

    def test_check_stock_available(self, subtests):
        """Test when the stock has ingredients available."""
        base_stock = [100, 100, 100]
        syrup_stock = [100, 100, 100, 100]

        # Test for `caramel milk tea`, `strawberry milk` and `plain latte`
        drinks = ["caramel milk tea", "strawberry milk", "latte"]
        for drink in drinks:
            with subtests.test(drink=drink):
                syrup, required_syrup = self.get_syrup(drink)
                _, required_base = self.get_base(drink, 20 if syrup else 30)

                assert (
                    skbin1.check_stock(
                        base_stock, syrup_stock, required_base, required_syrup
                    )
                    == True
                )

    def test_check_stock_unavailable(self):
        """Test when stock is not available."""
        base_stock = [0, 0, 0]
        syrup_stock = [0, 0, 0, 0]

        assert (
            skbin1.check_stock(
                base_stock, syrup_stock, [10 for _ in range(3)], [10 for _ in range(4)]
            )
            == False
        )

    def test_update_stock(self, subtests):
        """Test that updating stock is correctly done."""
        drinks = ["plain coffee", "strawberry milk", "milk tea"]
        for drink in drinks:
            with subtests.test(drink=drink):
                base_stock = [100, 100, 100]
                syrup_stock = [100, 100, 100, 100]
                base_orig = base_stock.copy()
                syrup_orig = syrup_stock.copy()
                syrup, required_syrup = self.get_syrup(drink)
                _, required_base = self.get_base(drink, 20 if syrup else 30)

                skbin1.update_stock(
                    base_stock, syrup_stock, required_base, required_syrup
                )

                assert all(
                    [
                        base_stock
                        == [x[0] - x[1] for x in zip(base_orig, required_base)],
                        syrup_stock
                        == [x[0] - x[1] for x in zip(syrup_orig, required_syrup)],
                    ]
                )
