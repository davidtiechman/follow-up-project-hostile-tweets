from schedule_publishing import Scheduler  # renamed scheduler.py to scheduler_service.py

if __name__ == "__main__":
    scheduler = Scheduler(batch_size=100, interval_minutes=1)
    scheduler.run()
