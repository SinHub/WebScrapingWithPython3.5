from urllib.robotparser import RobotFileParser

class Crawler:
    def __init__(self, seed_url, scrape_callback, cache, timeout, ignore_robots = True):
        pass
    
    def is_robot_friendly(self, user_agent):
        rp = rp = RobotFileParser()
        rp.set_url(urljoin(base_url, '/robots.txt'))
        rp.read()
        return rp.can_fetch(user_agent, url)