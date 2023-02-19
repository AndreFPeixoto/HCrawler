class Job:
    id = None

    def __init__(self, tag, download_path, total_pages, total_posts, last_page_downloaded, last_post_downloaded,
                 last_run, created_at, updated_at):
        self.tag = tag
        self.download_path = download_path
        self.total_pages = total_pages
        self.total_posts = total_posts
        self.last_page_downloaded = last_page_downloaded
        self.last_post_downloaded = last_post_downloaded
        self.last_run = last_run
        self.created_at = created_at
        self.updated_at = updated_at

    def info(self):
        return f"Tag: id={self.id} tag={self.tag} download_path={self.download_path} total_pages={self.total_pages} total_posts={self.total_posts} last_page_downloaded={self.last_page_downloaded} last_post_downloaded={self.last_post_downloaded} last_run={self.last_run} created_at={self.created_at} updated_at={self.updated_at}"
