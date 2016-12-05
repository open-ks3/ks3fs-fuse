/* Copyright (c) 2015 KingSoft.com, Inc. All rights reserved. */

#include <algorithm>
#include <errno.h>
#include <fcntl.h>
#include <stdexcept>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/time.h>
#include <unistd.h>
#include <sys/types.h>
#include <dirent.h>
#include <map>
#include "log.h"

#define gettid() syscall(__NR_gettid)

static const char *log_level_names[] = { "CRT", "ERR", "WAN", "INF",
                                         "TAC", "DBG" };
static const int64_t kMinInterval = 900; // 15 min
static const int64_t kDefaultInterval = 3600; // 1 hour

Log Log::logger_;

Log::Log(const std::string& path, const std::string& prefix, int level, int max_file_count)
{
    set_log_level(level);
    set_max_file_count(max_file_count);
    SetDefaultParam();
    SetLogPrefix(path, prefix);
}

Log::~Log()
{
    CloseLog();
}

void Log::set_log_level(int level)
{
    if (LL_FATAL <= level && level <= LL_DEBUG)
        log_level_ = level;
    else
        log_level_ = LL_DEBUG;
}

void Log::set_max_file_count(int file_count)
{
    if (0 < file_count)
        max_file_count_ = file_count;
    else
        max_file_count_ = 10;
}

void Log::SetDefaultParam()
{
    fd_ = -1;
    set_rotate_by_day(false);
    set_need_process_id(false);
    set_need_thread_id(true);
}

int Log::CompareTm(const struct tm& left, const struct tm& right) {
    int tmp = left.tm_year - right.tm_year;
    if (tmp != 0) {
        return tmp;
    }

    tmp = left.tm_mon - right.tm_mon;
    if (tmp != 0) {
        return tmp;
    }

    tmp = left.tm_mday - right.tm_mday;
    if (rotate_by_day_) {
        return tmp;
    }

    if (tmp != 0) {
        return tmp;
    }

    return left.tm_hour - right.tm_hour;
}

bool Log::SetLogPrefix(const std::string& path, const std::string& prefix)
{
    if (path.empty() || prefix.empty()) {
        return false;
    }

    struct stat st;
    if (-1 == stat(path.c_str(), &st)) {
        // mkdir 755
        if (-1 == mkdir(path.c_str(), S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH)) {
            return false;
        }
    }
    else if (!S_ISDIR(st.st_mode)) {
        return false;
    }

    prefix_ = prefix;
    path_ = path;
    path_ += "/";


    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    localtime_r(&(tv_now.tv_sec), &current_tm_);
    std::string sample_name = GetNewLogName(current_tm_);

    std::vector<std::string> valid_files;
    std::vector<std::string> file_list;
    GetFileList(path, &file_list);
    std::vector<std::string>::const_iterator it = file_list.begin();
    for (; it != file_list.end(); ++it) {
        const std::string& tmp_name = *it;
        if (tmp_name.find(prefix) != 0 || tmp_name.size() != sample_name.size()) {
            continue;
        }

        // start with prefix
        valid_files.push_back(tmp_name);
    }

    CloseLog();
    std::string last_log_name;
    std::string filename = DefaultLogName();
    if (FileExists(filename.c_str())) {
        struct stat buf;
        if (0 == stat(filename.c_str(), &buf)) {
            struct tm* local_time = localtime(&(buf.st_mtime));
            if (CompareTm(*local_time, current_tm_) < 0) {
                last_log_name = GetNewLogName(*local_time);
                valid_files.push_back(last_log_name);
            }
        }
    }

    std::sort(valid_files.begin(), valid_files.end());
    std::vector<std::string>::const_iterator it_valid = valid_files.begin();
    for (; it_valid != valid_files.end(); ++it_valid) {
        exist_files_.push_back(*it_valid);
    }

    return OpenLog(last_log_name, &fd_);
}

std::string Log::DefaultLogName() {
    std::string filename(path_);
    filename.append(prefix_);
    filename.append(".log");
    return filename;
}

std::string Log::GetNewLogName(const tm& tm_now)
{
    char buff[256];
    int buff_len = 0;
    if (rotate_by_day_) {
        buff_len = snprintf(buff, sizeof(buff), "%04d-%02d-%02d.00", tm_now.tm_year + 1900,
                            tm_now.tm_mon + 1, tm_now.tm_mday);
    } else {
        buff_len = snprintf(buff, sizeof(buff), "%04d-%02d-%02d.%02d", tm_now.tm_year + 1900,
                            tm_now.tm_mon + 1, tm_now.tm_mday, tm_now.tm_hour);
    }

    std::string filename(prefix_);
    filename.append("_");
    filename.append(buff, buff_len);
    filename.append(".log");
    return filename;
}

bool Log::OpenLog(const std::string& last_log_name, int* fd)
{
    std::string filename = DefaultLogName();
    if (!last_log_name.empty()) {
        std::string dest_file(path_);
        dest_file.append(last_log_name);
        rename(filename.c_str(), dest_file.c_str());
    }

    *fd = open(filename.c_str(), O_RDWR | O_CREAT | O_APPEND | O_LARGEFILE, 0644);
    if (*fd < 0) {
        fprintf(stderr, "failed to open file %s", filename.c_str());
        return false;
    }

    return true;
}

void Log::CloseLog()
{
    if (fd_ >= 0) {
        close(fd_);
        fd_ = -1;
    }
}

int Log::WriteData(const char *data, int size)
{
    int succ_size = 0;
    if (size <= 0)
        return 0;
    if (fd_ < 0)
        succ_size = ::write(2, data, size);
    else
        succ_size = ::write(fd_, data, size);

    return succ_size;
}

bool Log::GetFileList(const std::string& path,
        std::vector<std::string>* file_list) {
    file_list->clear();
    DIR* dir = opendir(path.c_str());
    if(NULL == dir) {
        return false;
    }
    struct dirent* dir_entry= NULL;
    struct dirent temp;

    while(readdir_r(dir, &temp, &dir_entry) == 0) {
        if (NULL == dir_entry) {
            break;
        }

        if (!strcmp(dir_entry->d_name,".") || !strcmp(dir_entry->d_name,"..")) {
            continue;
        }
        file_list->push_back(dir_entry->d_name);
    }
    closedir(dir);
    return true;
}

bool Log::FileExists(const std::string& file_name) {
    return access(file_name.c_str(), F_OK) == 0;
}

void Log::Write(int log_level, const char *fmt, ...)
{
    va_list va;
    va_start(va, fmt);
    Write(log_level, NULL, 0, NULL, fmt, va);
    va_end(va);
}

void Log::Write(int log_level, const char *filename, int line,
                const char *function, const char *fmt, ...)
{
    va_list va;
    va_start(va, fmt);
    Write(log_level, filename, line, function, fmt, va);
    va_end(va);
}


void Log::MaybeCreateNewLog() {
    ScopedLocker<MutexLock> lock(lock_);
    struct tm tm_now;
    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    localtime_r(&(tv_now.tv_sec), &tm_now);
    if (CompareTm(tm_now, current_tm_) <= 0) {
        return;
    }

    MaybeDeleteOldLogs();
    int tmp_fd = -1;
    std::string new_log_name = GetNewLogName(current_tm_);
    if (!OpenLog(new_log_name, &tmp_fd)) {
        return;
    }
    current_tm_.tm_year = tm_now.tm_year;
    current_tm_.tm_mon = tm_now.tm_mon;
    current_tm_.tm_mday = tm_now.tm_mday;
    current_tm_.tm_hour = tm_now.tm_hour;

    exist_files_.push_back(new_log_name);
    dup2(tmp_fd, fd_);
    close(tmp_fd);
}

void Log::Write(int log_level, const char *filename, int line,
                const char *function, const char *fmt, va_list args)
{
    if (log_level_ < log_level)
        return;

    struct tm tm_now;
    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    localtime_r(&(tv_now.tv_sec), &tm_now);
    if (current_tm_.tm_hour != tm_now.tm_hour) {
        MaybeCreateNewLog();
    }

    char buff[4096];
    uint32_t left = sizeof(buff);
    char* data = NULL;

    int buff_len = snprintf(buff, sizeof(buff), "[%s][%04d-%02d-%02d %02d:%02d:%02d %06ld]",
                            log_level_names[log_level], tm_now.tm_year + 1900,
                            tm_now.tm_mon + 1, tm_now.tm_mday, tm_now.tm_hour, tm_now.tm_min,
                            tm_now.tm_sec, tv_now.tv_usec);
    if (need_process_id_) {
        data = buff + buff_len;
        left = sizeof(buff) - buff_len;
        snprintf(data, left, "[%d]", getpid());
    }
    if (need_thread_id_) {
        buff_len = strlen(buff);
        data = buff + buff_len;
        left = sizeof(buff) - buff_len;
        //snprintf(data, left, "[%lu]", pthread_self());
        snprintf(data, left, "[%lu]", gettid());
    }

    if ((NULL != filename) && (line > 0) && (NULL != function)) {
        buff_len = strlen(buff);
        data = buff + buff_len;
        left = sizeof(buff) - buff_len;
        snprintf(data, left, "[%s:%s:%d]", filename, function, line);
    }

    buff_len = strlen(buff);
    data = buff + buff_len;
    *data = '[';
    data += 1;

    buff_len = strlen(buff);
    left = sizeof(buff) - buff_len - 2;
    vsnprintf(data, left, fmt, args);

    buff_len = strlen(buff);
    data = buff + buff_len;
    *data = ']';
    data += 1;
    *data = '\0';

    int size = strlen(buff);
    while (buff[size-1] == '\n')
        --size;
    buff[size] = '\n';
    buff[size+1] = '\0';

    size = strlen(buff);
    WriteData(buff, size);
}

void Log::MaybeDeleteOldLogs() {
    if ((int)exist_files_.size() <= max_file_count_) {
        return;
    }

    while ((int)exist_files_.size() > max_file_count_) {
        std::string file_name = exist_files_.front();
        exist_files_.pop_front();

        // delete oldest log
        std::string full_name(path_);
        full_name.append(file_name);
        unlink(full_name.c_str());
    }
}

