import time
import datetime
import socket
import json

from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (render, render_to_response, redirect, get_object_or_404)
from django.core.mail import (send_mail, BadHeaderError)
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.conf import settings
from django.db.models import (Q, Count)

from smartsearch.models import *
from smartsearch.forms import ContactForm
from smartsearch.utils.paginator import GenericPaginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Specialist
from .serializers import *
from django.http import Http404
from django.views.generic import ListView


def handler400(request):
    response = render_to_response('error_page.html', {'title': '400 Bad Request', 'message': '400'},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response


def handler403(request):
    response = render_to_response('error_page.html', {'title': '403 Permission Denied', 'message': '403'},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response


def handler404(request):
    response = render_to_response('error_page.html', {'title': '404 Not Found', 'message': '404'},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('error_page.html', {'title': '500 Server Error', 'message': '500'},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


class HomepageView(generic.ListView):
    queryset = Post.objects.published()
    template_name = 'smartsearch/smartsearch_home.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context_data = super(HomepageView, self).get_context_data(**kwargs)
        context_data['page_range'] = GenericPaginator(
            self.queryset,
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data



class DetailPostView(generic.DetailView):
    model = Post
    template_name = 'smartsearch/smartsearch_detail.html'

    def get_client_ip(self):
        ip = self.request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            ip = ip.split(", ")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR", "")
        return ip

    def visitorCounter(self):
        try:
            Visitor.objects.get(
                post=self.object,
                ip=self.request.META['REMOTE_ADDR']
            )
        except ObjectDoesNotExist:
            dns = str(socket.getfqdn(
                self.request.META['REMOTE_ADDR']
            )).split('.')[-1]
            try:
                # trying for localhost: str(dns) == 'localhost',
                # trying for production: int(dns)
                if str(dns) == 'localhost':
                    visitor = Visitor(
                        post=self.object,
                        ip=self.request.META['REMOTE_ADDR']
                    )
                    visitor.save()
                else:
                    pass
            except ValueError:
                pass
        return Visitor.objects.filter(post=self.object).count()

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.publish == False:
            if request.user.is_anonymous() or \
                    request.user != obj.author.user:
                return redirect('homepage')
            else:
                return super(DetailPostView, self).dispatch(
                    request, *args, **kwargs
                )
        elif request.GET.get('format') == 'json':
            get_cover = lambda obj: None if obj.cover == None \
                or obj.cover == '' \
                else 'https://{0}{1}{2}'.format(
                    request.get_host(),
                    settings.MEDIA_URL,
                    obj.cover
                )
            data = dict(
                title=obj.title,
                url='https://{0}/smartsearch/{1}'.format(
                    request.get_host(),
                    obj.slug
                ),
                cover=get_cover(obj),
                author=obj.author.user.username,
                created=str(obj.created)[:19],
                modified=str(obj.modified)[:19],
                tags=[
                    {'title': t.title, 'slug': t.slug}
                    for t in obj.tags.all()
                ],
                description=obj.description,
                visitors=obj.total_visitors
            )
            return HttpResponse(
                json.dumps(data),
                content_type='application/json'
            )
        else:
            return super(DetailPostView, self).dispatch(
                request, *args, **kwargs
            )

    def get_context_data(self, **kwargs):
        context_data = super(DetailPostView, self).get_context_data(**kwargs)
        related_posts = Post.objects.filter(
            tags__in=list(self.object.tags.all())
        ).exclude(id=self.object.id).distinct()
        context_data['related_posts'] = related_posts[:5]  # limit for post
        context_data['get_client_ip'] = self.get_client_ip()
        context_data['visitor_counter'] = self.visitorCounter()
        return context_data


class SearchPostsView(generic.ListView):
    template_name = 'smartsearch/smartsearch_search.html'
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q')
        try:
            search_posts = Post.objects.published().filter(
                Q(title__icontains=self.query) |
                Q(description__icontains=self.query) |
                Q(keywords__icontains=self.query) |
                Q(meta_description__icontains=self.query)
            ).order_by('-created').order_by('-id')
            return search_posts
        except:
            return Post.objects.published()

    def get_context_data(self, **kwargs):
        context_data = super(SearchPostsView, self).get_context_data(**kwargs)
        context_data['query'] = self.query
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class AuthorPostsView(generic.ListView):
    template_name = 'smartsearch/smartsearch_posts_author.html'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']
        self.author = get_object_or_404(Author, user__username=username)
        posts_author = Post.objects.published().filter(
            author=self.author
        ).order_by('-created').order_by('-id')
        return posts_author

    def get_context_data(self, **kwargs):
        context_data = super(AuthorPostsView, self).get_context_data(**kwargs)
        context_data['author'] = self.author
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class TagPostsView(generic.ListView):
    template_name = 'smartsearch/smartsearch_posts_tag.html'
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=slug)
        results_filter = Post.objects.published().filter(
            tags=self.tag
        ).order_by('-created').order_by('-id')
        return results_filter

    def get_context_data(self, **kwargs):
        context_data = super(TagPostsView, self).get_context_data(**kwargs)
        context_data['tag'] = self.tag
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class DetailPageView(generic.DetailView):
    model = Page
    template_name = 'smartsearch/smartsearch_page.html'


class SitemapView(generic.ListView):
    queryset = Post.objects.published()
    template_name = 'smartsearch/smartsearch_sitemap.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context_data = super(SitemapView, self).get_context_data(**kwargs)
        context_data['page_range'] = GenericPaginator(
            self.queryset,
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class ContactView(generic.TemplateView):
    template_name = 'smartsearch/smartsearch_contact.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['form'].is_valid():
            cd = context['form'].cleaned_data
            subject = cd['subject']
            from_email = cd['email']
            message = cd['message']

            try:
                send_mail(
                    subject + " from {}".format(from_email),
                    message,
                    from_email,
                    [settings.EMAIL_HOST_USER]
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            ctx = {
                'success': """Thankyou, We appreciate that you've
                taken the time to write us.
                We'll get back to you very soon.
                Please come back and see us often."""
            }
            return render(request, self.template_name, ctx)
        return super(generic.TemplateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        form = ContactForm(self.request.POST or None)
        context['form'] = form
        return context


class TrendingPostsView(generic.ListView):
    template_name = 'smartsearch/smartsearch_trending_posts.html'

    def get_queryset(self):
        posts = Post.objects.published()
        top_posts = Visitor.objects.filter(post__in=posts)\
            .values('post').annotate(visit=Count('post__id'))\
            .order_by('-visit')

        list_pk_top_posts = [pk['post'] for pk in top_posts]
        filter_posts = list(Post.objects.published().filter(pk__in=list_pk_top_posts))
        sorted_posts = sorted(filter_posts, key=lambda i: list_pk_top_posts.index(i.pk))

        self.get_filter = self.request.GET.get('filter')
        now_year = time.strftime("%Y")
        now_month = time.strftime("%m")
        now_date = datetime.date.today()
        start_week = now_date - datetime.timedelta(7)
        end_week = start_week + datetime.timedelta(7)

        if self.get_filter == 'week':
            filter_posts = list(Post.objects.published()
                                .filter(pk__in=list_pk_top_posts)
                                .filter(created__date__range=[start_week, end_week])
                                )
            sorted_posts = sorted(filter_posts, key=lambda i: list_pk_top_posts.index(i.pk))

        elif self.get_filter == 'month':
            filter_posts = list(Post.objects.published()
                                .filter(pk__in=list_pk_top_posts)
                                .filter(created__month=now_month)
                                .filter(created__year=now_year)
                                )
            sorted_posts = sorted(filter_posts, key=lambda i: list_pk_top_posts.index(i.pk))

        elif self.get_filter == 'year':
            filter_posts = list(Post.objects.published()
                                .filter(pk__in=list_pk_top_posts)
                                .filter(created__year=now_year)
                                )
            sorted_posts = sorted(filter_posts, key=lambda i: list_pk_top_posts.index(i.pk))

        else:
            self.get_filter == 'global'
            sorted_posts = sorted_posts
        return sorted_posts[:20]  # Return 20 posts only

    def get_context_data(self, **kwargs):
        context_data = super(TrendingPostsView, self).get_context_data(**kwargs)
        context_data['filter'] = self.get_filter
        return context_data

		
		
# Lists all specialist or creates a new one
# specialist/
class SpecialistListView(generic.ListView):
    model = Specialist
#    context_object_name = 'specialist_list'   # your own name for the list as a template variable
    template_name = 'smartsearch/smartsearch_specialist_list.html'  # Specify your own template name/location

    def get_queryset(self):	
        #return Specialist.objects.filter(speciality__icontains='medecine') # Get 5 books containing the title war
        return Specialist.objects.all()


class PostList(APIView):

    def get(self, request):
        posts = Post.objects.filter(specialist=request.GET.__getitem__('specialist'))
        serializer = PostSerializer(posts, many=True)

        for i in range(len(serializer.data)):
            rates_json= {}   
            rates = Rate.objects.filter(post=serializer.data[i]['id']).values('rate_name', 'rate_value')

            for j in range(len(rates)):
                 rates_json[rates[j]['rate_name']]=str(str(rates[j]['rate_value']))
            serializer.data[i]["rates"] = rates_json
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        print(request.data)
        serializer = SpecialistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RateList(APIView):
    def post(self, request):
        print(request.data)
        serializer = SpecialistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialistList(APIView):

    def get(self, request):
        #specialists = Specialist.objects.all()
        specialists = Specialist.objects.filter(speciality=request.GET.__getitem__('speciality'))
        speciality = Speciality.objects.filter(id=request.GET.__getitem__('speciality')).values('title','domain')
        domain = Domain.objects.filter(id=speciality[0]['domain']).values('title', 'about')
        serializer = SpecialistSerializer(specialists, many=True)
        if (len(serializer.data)>0):
            serializer.data[0]['speciality']=str(speciality[0])
            serializer.data[0]['domain']=str(domain[0])
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        print(request.data)
        serializer = SpecialistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialityList(APIView):

    def get(self, request):
        specialities = Speciality.objects.filter(domain=request.GET.__getitem__('domain'))
        domain = Domain.objects.filter(id=request.GET.__getitem__('domain')).values('title', 'about')
        serializer = SpecialitySerializer(specialities, many=True)
        for i in range(len(serializer.data)):
            serializer.data[i]['domain']=str(domain[0])

        return JsonResponse(serializer.data, safe=False)


class SpecialityAllList(APIView):

    def get(self, request):
        specialities = Speciality.objects.all()
        serializer = SpecialitySerializer(specialities, many=True)
        for i in range(len(serializer.data)):
            domain = Domain.objects.filter(id=int(serializer.data[i]['domain'])).values('title', 'about')
            serializer.data[i]['domain']=str(domain[0])

        return JsonResponse(serializer.data, safe=False)


class DomainList(APIView):

    def get(self, request):
        domains = Domain.objects.all().values('id', 'title', 'about', 'imagePath')
        serializer = DomainSerializer(domains, many=True)
        return JsonResponse(serializer.data, safe=False)


class SpecialistDetail(APIView):
    def get_object(self, pk):
        try:
            return Specialist.objects.get(pk=pk)
        except Specialist.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = SpecialistSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = SpecialistSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestView(APIView):
  #  Specialist.objects.filter(name="Hechmi hamdi").delete()
    print(Specialist.objects)


class SpecialistDetailView(generic.DetailView):
    model = Specialist
    template_name = 'smartsearch/smartsearch_specialist_detail.html'



# Lists all domains or creates a new one
class DomainsListView(generic.ListView):
    model = Domain
    context_object_name = 'domain_list'   # your own name for the list as a template variable
    template_name = 'smartsearch/smartsearch_domains_list.html'

    def get_queryset(self): 
        return Domain.objects.all()


# Lists all domains or creates a new one
class RateView(generic.ListView):
    model = Rate
    context_object_name = 'rate_list'   # your own name for the list as a template variable
    template_name = 'smartsearch/smartsearch_domains_list.html'

    def get_queryset(self): 
        return Domain.objects.all()


class DomainSpecialitiesListView(generic.ListView):
    template_name = 'smartsearch/smartsearch_speciality_list.html'
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        self.domain = get_object_or_404(Domain, pk=pk)
        results_filter = Speciality.objects.filter(domain=self.domain)
        return results_filter

    def get_context_data(self, **kwargs):
        context_data = super(DomainSpecialitiesListView, self).get_context_data(**kwargs)
        context_data['domain'] = self.domain
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data


class SpecialistesListView(generic.ListView):
    template_name = 'smartsearch/smartsearch_specialistes_list.html'
    paginate_by = 10

    # for filtering list of specialists on speciality
    def get_queryset(self):
        pk = self.kwargs['pk']
        self.speciality = get_object_or_404(Speciality, pk=pk)
        results_filter = Specialist.objects.filter(speciality=self.speciality)
        return results_filter

    # for pagination
    def get_context_data(self, **kwargs):
        context_data = super(SpecialistesListView, self).get_context_data(**kwargs)
        context_data['speciality'] = self.speciality
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data



class SpecialistPostsView(generic.ListView):
    template_name = 'smartsearch/smartsearch_posts_specialist.html'
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        self.specialist = get_object_or_404(Specialist, pk=pk)
        posts_specialist = Post.objects.published().filter(
            specialist=self.specialist
        ).order_by('-created').order_by('-id')
        return posts_specialist

    def get_context_data(self, **kwargs):
        context_data = super(SpecialistPostsView, self).get_context_data(**kwargs)
        context_data['specialist'] = self.specialist
        context_data['page_range'] = GenericPaginator(
            self.get_queryset(),
            self.paginate_by,
            self.request.GET.get('page')
        ).get_page_range()
        return context_data
