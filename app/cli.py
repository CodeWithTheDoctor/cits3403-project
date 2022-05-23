import click
from app import db
from app.models import Puzzle, User, User_Puzzle


def register(app):
    @app.cli.command("add-puzzle")
    @click.argument("config")
    def add_puzzle(config):
        """Enter the config for a new puzzle"""
        p = Puzzle(config=config)
        try:
            db.session.add(p)
            db.session.commit()
            print("Puzzle successfully added")
        except:
            print("Error adding new puzzle")
            db.session.rollback()

    @app.cli.command("delete-puzzle")
    @click.argument("puzzle_id")
    def delete_puzzle(puzzle_id):
        """Delete puzzle by  id"""

        p = Puzzle.query.get(puzzle_id)

        if p is None:
            print(f"ERROR: No puzzle exists by {puzzle_id}")
            return

        try:
            db.session.delete(p)
            db.session.commit()
            print(f"Puzzle: {puzzle_id} successfully deleted")
        except Exception as e:
            print("Error encountered while deleting")
            print(e)

    @app.cli.command("puzzles")
    def puzzles():
        """Show all puzzles"""
        puzzles = Puzzle.query.all()

        for puzzle in puzzles:
            print(f"Puzzle: {puzzle.id} has config {puzzle.config}")

    @app.cli.command("users")
    def users():
        """Show all users"""
        users = User.query.all()

        for user in users:
            print(f"User: {user.id} has username {user.username}")

    @app.cli.command("delete-user")
    @click.argument("user_id")
    def delete_user(user_id):
        """Delete user by id"""
        u = User.query.get(user_id)

        if u is None:
            print(f"ERROR: No puzzle exists by {user_id}")
            return

        try:
            db.session.delete(u)
            db.session.commit()
            print(f"User: {user_id} successfully deleted")
        except Exception as e:
            print("Error encountered while deleting")
            print(e)
            
            
    @app.cli.command("user-puzzle")
    @click.argument("puzzle_id")
    def getLeaderboard(puzzle_id):
        results = User_Puzzle.query.filter_by(puzzle_id=puzzle_id).order_by(User_Puzzle.time).all()
        print(results)
        
        if results is None:
            print(f"ERROR: No puzzle exists by {user_id}")
            return
        
        for result in results:
            print(f"resutlt {result.id}: user - {result.user_id} : puzzle - {puzzle_id}")

        
    @app.cli.command("results")
    def results():
        """Show all users"""
        results = User_Puzzle.query.all()

        for result in results:
            print(f"user - {result.user_id} : puzzle - {result.puzzle_id} : time - {result.time}")
