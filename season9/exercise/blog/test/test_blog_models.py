import pytest
from django.utils import timezone
from datetime import timedelta
from blog.models import BlogPost

# --------------- Fixtures ---------------

@pytest.fixture
def sample_blog_post():
    """Fixture that creates and returns a blog post."""
    return BlogPost.objects.create(
        title="Test Blog Post",
        content="This is the content of the test blog post.",
        author="Test Author"
    )

@pytest.fixture
def old_blog_post():
    """Fixture that creates a blog post from 10 days ago."""
    ten_days_ago = timezone.now() - timedelta(days=10)
    return BlogPost.objects.create(
        title="Old Blog Post",
        content="This is an old blog post.",
        author="Test Author",
        published_date=ten_days_ago
    )

@pytest.fixture
def long_content_blog_post():
    """Fixture that creates a blog post with long content."""
    long_content = "Lorem ipsum dolor sit amet, " * 20  # Long content
    return BlogPost.objects.create(
        title="Long Content Blog Post",
        content=long_content,
        author="Test Author"
    )

# --------------- Basic CRUD Tests ---------------

@pytest.mark.django_db
def test_blog_post_creation(sample_blog_post):
    """Test that a blog post can be created correctly."""
    assert sample_blog_post.title == "Test Blog Post"
    assert sample_blog_post.content == "This is the content of the test blog post."
    assert sample_blog_post.author == "Test Author"
    assert sample_blog_post.published_date is not None

@pytest.mark.django_db
def test_blog_post_str_representation(sample_blog_post):
    """Test the string representation of a blog post."""
    expected_str = "Test Blog Post by Test Author"
    assert str(sample_blog_post) == expected_str

@pytest.mark.django_db
def test_blog_post_update(sample_blog_post):
    """Test that a blog post can be updated."""
    sample_blog_post.title = "Updated Title"
    sample_blog_post.save()
    
    # Retrieve the blog post again from the database
    updated_post = BlogPost.objects.get(pk=sample_blog_post.pk)
    assert updated_post.title == "Updated Title"

@pytest.mark.django_db
def test_blog_post_deletion(sample_blog_post):
    """Test that a blog post can be deleted."""
    post_id = sample_blog_post.pk
    sample_blog_post.delete()
    
    # Check that the blog post no longer exists
    with pytest.raises(BlogPost.DoesNotExist):
        BlogPost.objects.get(pk=post_id)

# --------------- Custom Method Tests ---------------

@pytest.mark.django_db
def test_is_recent_with_new_post(sample_blog_post):
    """Test the is_recent method with a new blog post."""
    assert sample_blog_post.is_recent() is True

@pytest.mark.django_db
def test_is_recent_with_old_post(old_blog_post):
    """Test the is_recent method with an old blog post."""
    assert old_blog_post.is_recent() is False

@pytest.mark.django_db
def test_get_short_preview_with_short_content(sample_blog_post):
    """Test the get_short_preview method with content shorter than max_length."""
    preview = sample_blog_post.get_short_preview(max_length=200)
    assert preview == sample_blog_post.content
    assert "..." not in preview

@pytest.mark.django_db
def test_get_short_preview_with_long_content(long_content_blog_post):
    """Test the get_short_preview method with content longer than max_length."""
    preview = long_content_blog_post.get_short_preview(max_length=50)
    assert len(preview) <= 53  # 50 chars + "..."
    assert preview.endswith("...")
    assert preview.startswith(long_content_blog_post.content[:10])

# --------------- Parametrized Tests ---------------

@pytest.mark.django_db
@pytest.mark.parametrize(
    "title,content,author", 
    [
        ("Post 1", "Content 1", "Author 1"),
        ("Post 2", "Content 2", "Author 2"),
        ("", "Empty title post", "Author 3"),  # Test with empty title
        ("Unicode Title 🚀", "Content with Unicode 🎮", "Author 🌟"),  # Test with Unicode
    ]
)
def test_create_blog_posts_parametrized(title, content, author):
    """Test creating blog posts with different parameters."""
    post = BlogPost.objects.create(
        title=title,
        content=content,
        author=author
    )
    assert post.title == title
    assert post.content == content
    assert post.author == author

# --------------- Query Tests ---------------

@pytest.mark.django_db
def test_query_blog_posts():
    """Test querying blog posts."""
    # Create multiple blog posts
    BlogPost.objects.create(title="Post 1", content="Content 1", author="Author 1")
    BlogPost.objects.create(title="Post 2", content="Content 2", author="Author 2")
    BlogPost.objects.create(title="Post 3", content="Content 3", author="Author 1")
    
    # Test basic count
    assert BlogPost.objects.count() == 3
    
    # Test filtering by author
    author_1_posts = BlogPost.objects.filter(author="Author 1")
    assert author_1_posts.count() == 2
    
    # Test ordering (default is -published_date from Meta class)
    all_posts = list(BlogPost.objects.all())
    # The most recently created post should be first due to ordering in Meta
    assert all_posts[0].title == "Post 3"