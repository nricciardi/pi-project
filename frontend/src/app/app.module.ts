import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HttpClient } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FooterComponent } from './widget/footer/footer.component';
import { HeaderComponent } from './widget/header/header.component';
import { PageNotFoundComponent } from './page/page-not-found/page-not-found.component';
import { TaskPreviewComponent } from './widget/task/task-preview/task-preview.component';
import { TaskPreviewListComponent } from './widget/task/task-preview-list/task-preview-list.component';
import { DashboardComponent } from './page/dashboard/dashboard.component';
import { TranslateLoader, TranslateModule, TranslateService } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { PageHeadingComponent } from './widget/page-heading/page-heading.component';
import { LoaderComponent } from './widget/loader/loader.component';
import { LoginComponent } from './page/login/login.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ErrorAlertComponent } from './widget/alert/error-alert/error-alert.component';
import { HomeComponent } from './page/home/home.component';
import { TaskStatusSideBannerComponent } from './widget/task/task-status-side-banner/task-status-side-banner.component';
import { SidebarComponent } from './widget/sidebar/sidebar.component';
import { TestComponent } from './page/test/test.component';
import { TextAvatarComponent } from './widget/avatar/text-avatar/text-avatar.component';


@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    SidebarComponent,
    HeaderComponent,
    PageNotFoundComponent,
    TaskPreviewComponent,
    TaskPreviewListComponent,
    DashboardComponent,
    PageHeadingComponent,
    LoaderComponent,
    LoginComponent,
    ErrorAlertComponent,
    HomeComponent,
    TaskStatusSideBannerComponent,
    TestComponent,
    TextAvatarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    TranslateModule.forRoot({
      defaultLanguage: 'en',
      useDefaultLang: true,
      loader: {
        provide: TranslateLoader,
        useFactory: (http: HttpClient) => {
          return new TranslateHttpLoader(http, './assets/i18n/', '.json');
        },
        deps: [HttpClient]
      }
    }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
