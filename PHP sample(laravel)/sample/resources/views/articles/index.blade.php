@extends('layouts.app')

@section('content')

    <h1>Articles</h1>
    @if(count($articles) > 0)
    <ul class="list-group">  
        
        @foreach($articles as $article)
            <li class="list-group-item">
                
                    <h3><a href="\articles\{{$article->id}}">{{$article->title}}</a></h3>
            <small>Written on {{$article->created_at}}, author: {{$article->user->name}}</small>
                
            </li>
        @endforeach
    </ul>
    {{$articles->links()}}

    @else
        <p>No articles found</p>
    @endif

@endsection