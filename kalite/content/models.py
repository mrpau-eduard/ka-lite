"""
Models for storing content in structured trees with topic nodes.

Contents are editable by users, and thus there is a Draft inheritor for
different node types which is detached from the tree.

Current limitations:
 - A user cannot draft a different location in the tree.
 - Previous tree attachments are not maintained automatically, however
   leaving a copy of a node in a previous location with deleted=True
   is possible

Initially, this is thought to store all content as we start to only use JSON
data for importing and exporting. This is a long-term goal.

YAGNI (You Aren't Going to Need It): Much meta data is possible, please do not
add fields before a specific use case has occurred.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey


class TopicTree(MPTTModel):
    """Base model for all trees / channels"""
    name = models.CharField(
        max_length=255,
        verbose_name=_("name / title for node"),
        help_text=_("Displayed to the user"),
    )
    editors = models.ManyToManyField(
        'auth.User',
        verbose_name=_("editors"),
        help_text=_("User accounts with full rights to edit tree"),
    )
    root_node = models.ForeignKey(
        'Node',
        verbose_name=_("root node"),
        help_text=_(
            "The starting point for the tree, the title of it is the "
            "title shown in the menu"
        ),
    )
    
    class Meta:
        verbose_name = _("Topic tree")
        verbose_name_plural = _("Topic trees")


class NodeData(models.Model):
    """
    Abstract model of fields belonging to all nodes.
    
    This model is there, because nodes can be removed from their and thus
    not belong to a tree (in draft mode etc.)
    """

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("modified"))

    name = models.CharField(
        max_length=50,
        verbose_name=_("name"),
        help_text=_("Name of node to be displayed to the user in the menu"),
    )
    icon = models.CharField(
        max_length=24,
        choices=[  # Made up choices for non-existing icon set
            ('book', _('book')),
            ('school', _('school')),
            ('video', _('video')),
            ('math', _('math symbol')),
            ('chemistry', _('chemistry/science symbol')),
            ('astronomy', _('astronomy symbol')),
            ('picture-frame', _('picture frame')),
            ('check-mark', _('exercise icon')),
        ],
        verbose_name=_("icon"),
        help_text=_("Icon is next to the name in the menu"),
    )

    class Meta:
        abstract = True


class Node(MPTTModel, NodeData):
    """
    By default, all nodes have a title and can be used as a topic.
    """
    published = models.BooleanField(
        default=False,
        verbose_name=_("Published"),
        help_text=_("If published, students can access this item"),
    )
    deleted = models.BooleanField(
        default=False,
        verbose_name=_("Deleted"),
        help_text=_(
            "Indicates that the node has been deleted, and should only "
            "be retrievable through the admin backend"
        ),
    )
    sort_order = models.FloatField(
        max_length=50,
        unique=True,
        default=0,
        verbose_name=_("sort order"),
        help_text=_("Ascending, lowest number shown first"),
    )
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    @property
    def has_draft(self):
        return self.draft_set.all().exists()
    
    @property
    def get_draft(self):
        """
        NB! By contract, only one draft should always exist per node, this is
        enforced by the OneToOneField relation.
        :raises: Draft.DoesNotExist and Draft.MultipleObjectsReturned
        """
        return Draft.objects.get(publish_in=self)
    
    class MPTTMeta:
        order_insertion_by = ['sort_order']

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        # Do not allow two nodes with the same name on the same level
        unique_together = ('parent', 'name')


class Draft(models.Model):
    """
    This model is not abstract in order to have a generic way to access
    drafts and attach them to nodes
    """
    publish_in = models.OneToOneField(
        'Node',
        verbose_name=_("Node to attach to if published"),
    )


class Content(models.Model):
    """
    Abstract model for content data, fields that are shared across videos,
    exercises, and books...
    """
    
    author = models.CharField(
        max_length=255,
        verbose_name=_("author(s)"),
        help_text=_("Name of the author(s) of book/movie/exercise"),
    )
    license_owner = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("license owner(s)"),
        help_text=_("Organization of person who holds the essential rights"),
    )
    published_on = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("when published"),
        help_text=_(
            "If applicable, state when this work was first published (not on "
            "this platform, but for its original publication)."
        ),
    )
    retrieved_on = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("when retrieved/downloaded"),
        help_text=_(
            "Should be automatically filled in when an item is downloaded ",
            "from its source of origin, either manually by user or "
            "automatically by script."
        ),
    )
    license = models.ForeignKey(
        'ContentLicense',
        verbose_name=_("license"),
        help_text=_("License under which the work is distributed"),
    )
    thumbnail = models.ImageField(
        upload_to='contents/video/thumbnails/',
        verbose_name=_("video thumbnail"),
        help_text=_("Automatically created when new video is uploaded"),
    )
    
    class Meta:
        abstract = True


class ContentVideo(Content):
    """
    Abstract model for video data
    """
    
    video_file = models.FileField(
        blank=True,
        null=True,
        upload_to='contents/video/thumbnails/',
        verbose_name=_("video file"),
        help_text=_("Upload video here"),
    )
    
    class Meta:
        abstract = True


class ContentVideoNode(Node, ContentVideo):
    
    class Meta:
        verbose_name = _("Video node")
        verbose_name_plural = _("Video node")


class ContentVideoDraft(Draft, ContentVideo):

    class Meta:
        verbose_name = _("Video draft")
        verbose_name_plural = _("Video drafts")


class ContentPDF(Content):
    """
    Abstract model for video data
    """
    
    pdf_file = models.FileField(
        blank=True,
        null=True,
        upload_to='contents/video/thumbnails/',
        verbose_name=_("video file"),
        help_text=_("Upload video here"),
    )

    class Meta:
        abstract = True


class ContentPDFNode(Node, ContentPDF):

    class Meta:
        verbose_name = _("PDF node")
        verbose_name_plural = _("PDF nodes")


class ContentPDFDraft(Draft, ContentPDF):

    class Meta:
        verbose_name = _("PDF draft")
        verbose_name_plural = _("PDF drafts")


class Exercise(Content):
    """
    Abstract class for Exercise data. Is used both as a node in a
    Topic Tree
    """
    
    class Meta:
        abstract = True


class ExerciseNode(Node, Exercise):

    class Meta:
        verbose_name = _("Exercise node")
        verbose_name_plural = _("Exercise nodes")


class ExerciseDraft(Draft, Exercise):
    
    class Meta:
        verbose_name = _("Exercise draft")
        verbose_name_plural = _("Exercise drafts")


class ContentLicense(models.Model):
    
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("Name of license, e.g. 'Creative Commons Share-Alike 2.0'")
    )