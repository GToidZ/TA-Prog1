import pytest
from io import StringIO
from difflib import SequenceMatcher


def test_demo_skbin1(capsys, monkeypatch):
    inputs = StringIO("4\n")
    monkeypatch.setattr("sys.stdin", inputs)

    import skbin1

    expected_output = """Drink menu:
1. plain coffee
2. caramel coffee
3. brown sugar coffee
4. latte
5. caramel latte
6. brown sugar latte
7. plain tea
8. brown sugar tea
9. strawberry tea
10. lychee tea
11. milk tea
12. caramel milk tea
13. brown sugar milk tea
14. plain milk
15. caramel milk
16. brown sugar milk
17. strawberry milk
=====================
At the beginning, here are ingredient stocks...
coffee: 50, tea: 50, milk: 100
caramel: 20, brown sugar: 20, strawberry: 20, lychee: 20
=====================
Enter drink index: >>> You order latte
=====================
Needed ingredients:
coffee: 15, tea: 0, milk: 15
caramel: 0, brown sugar: 0, strawberry: 0, lychee: 0
After order, update ingredient stocks...
coffee: 35, tea: 50, milk: 85
caramel: 20, brown sugar: 20, strawberry: 20, lychee: 20
=====================
Your order is successful. Price of your drink = 35
Revenue : 35 Baht
"""
    captured = capsys.readouterr()
    similarity = SequenceMatcher(None, captured.out, expected_output).ratio()
    assert similarity >= 0.8, f"failing demo, similarity {similarity} too weak"


def test_demo_skbin2(capsys, monkeypatch):
    inputs = StringIO("4\n16\n3\n14\n8")
    monkeypatch.setattr("sys.stdin", inputs)

    import skbin2

    expected_output = """Drink menu:
1. plain coffee
2. caramel coffee
3. brown sugar coffee
4. latte
5. caramel latte
6. brown sugar latte
7. plain tea
8. brown sugar tea
9. strawberry tea
10. lychee tea
11. milk tea
12. caramel milk tea
13. brown sugar milk tea
14. plain milk
15. caramel milk
16. brown sugar milk
17. strawberry milk
=====================
At the beginning, here are ingredient stocks...
coffee: 50, tea: 50, milk: 100
caramel: 20, brown sugar: 20, strawberry: 20, lychee: 20
=====================
How many drinks? Enter drink index #1: >>> You order brown sugar milk
=====================
Needed ingredients:
coffee: 0, tea: 0, milk: 20
caramel: 0, brown sugar: 10, strawberry: 0, lychee: 0
After order, update ingredient stocks...
coffee: 50, tea: 50, milk: 80
caramel: 20, brown sugar: 10, strawberry: 20, lychee: 20
=====================
Your order is successful. Price of your drink = 30
Revenue : 30 Baht
=====================
Enter drink index #2: >>> You order brown sugar coffee
=====================
Needed ingredients:
coffee: 20, tea: 0, milk: 0
caramel: 0, brown sugar: 10, strawberry: 0, lychee: 0
After order, update ingredient stocks...
coffee: 30, tea: 50, milk: 80
caramel: 20, brown sugar: 0, strawberry: 20, lychee: 20
=====================
Your order is successful. Price of your drink = 30
Revenue : 60 Baht
=====================
Enter drink index #3: >>> You order plain milk
=====================
Needed ingredients:
coffee: 0, tea: 0, milk: 30
caramel: 0, brown sugar: 0, strawberry: 0, lychee: 0
After order, update ingredient stocks...
coffee: 30, tea: 50, milk: 50
caramel: 20, brown sugar: 0, strawberry: 20, lychee: 20
=====================
Your order is successful. Price of your drink = 25
Revenue : 85 Baht
=====================
Enter drink index #4: >>> You order brown sugar tea
=====================
Needed ingredients:
coffee: 0, tea: 20, milk: 0
caramel: 0, brown sugar: 10, strawberry: 0, lychee: 0
=====================
Your order is not successful
=====================
Revenue : 85 Baht
=====================
Sale : 3 Drinks
Final Revenue : 85 Baht
List of Successful Drinks:
1. brown sugar milk : 30 Baht
2. brown sugar coffee : 30 Baht
3. plain milk : 25 Baht
"""
    captured = capsys.readouterr()
    similarity = SequenceMatcher(None, captured.out, expected_output).ratio()
    assert similarity >= 0.7, f"failing demo, similarity {similarity} too weak"
