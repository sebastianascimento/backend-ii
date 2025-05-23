import pytest
from django.urls import reverse
from blog.models import BlogPost

@pytest.mark.django_db
def test_blog_list_view(client):
    """Test the blog list view that displays all blog posts."""
    # Create test blog posts
    BlogPost.objects.create(
        title="First Post", 
        content="First post content",
        author="Author 1"
    )
    BlogPost.objects.create(
        title="Second Post", 
        content="Second post content",
        author="Author 2"
    )
    
    # Get the response from the blog list view
    url = reverse('blog:post_list')  # Assuming you've defined this URL pattern
    response = client.get(url)
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that our blog posts are in the context
    assert len(response.context['posts']) == 2
    
    # Check that posts are in the response content
    content = response.content.decode()
    assert "First Post" in content
    assert "Second Post" in content

@pytest.mark.django_db
def test_blog_detail_view(client):
    """Test the blog detail view that displays a single blog post."""
    # Create a test blog post
    post = BlogPost.objects.create(
        title="Detail Test Post", 
        content="Detailed content for testing",
        author="Test Author"
    )
    
    # Get the response from the blog detail view
    url = reverse('blog:post_detail', kwargs={'pk': post.pk})
    response = client.get(url)
    
    # Check that the response is successful
    assert response.status_code == 200
    
    # Check that our blog post is in the context
    assert response.context['post'].title == "Detail Test Post"
    
    # Check that post content is in the response
    content = response.content.decode()
    assert "Detail Test Post" in content
    assert "Detailed content for testing" in content