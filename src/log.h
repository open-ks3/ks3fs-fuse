/**
 * Copyright (c) 2015 KingSoft.com, Inc. All rights reserved.
 *
 * File name: log.h
 * Description: log class and options
 * Date: 2015-5-11
 */

#ifndef _KYLIN_LIBS_LOG_LOG_H_
#define _KYLIN_LIBS_LOG_LOG_H_

#include <list>
#include <stdarg.h>
#include <pthread.h>
#include <stdint.h>
#include <string>
#include <string.h>
#include <vector>

#define LL_FATAL                 0
#define LL_ERROR                 1
#define LL_WARNING               2
#define LL_NOTICE                3
#define LL_TRACE                 4
#define LL_DEBUG                 5

#define MSG_FATAL                LL_FATAL, __FILE__, __LINE__, __FUNCTION__
#define MSG_ERROR                LL_ERROR, __FILE__, __LINE__, __FUNCTION__
#define MSG_WARNING              LL_WARNING, __FILE__, __LINE__, __FUNCTION__
#define MSG_NOTICE               LL_NOTICE, __FILE__, __LINE__, __FUNCTION__
#define MSG_TRACE                LL_TRACE, __FILE__, __LINE__, __FUNCTION__
#define MSG_DEBUG                LL_DEBUG, __FILE__, __LINE__, __FUNCTION__

#define LOGGER                   Log::logger_
//#define LOGV(level, fmt, args...) if (level <= LOGGER.log_level()) LOGGER.Write(level, __FILE__, __LINE__, __FUNCTION__, fmt, ##args)
#define LOGV(level, fmt, args...) if (level <= LOGGER.log_level()) LOGGER.Write(level, strrchr(__FILE__, '/') ? (strrchr(__FILE__, '/') + 1):__FILE__, __LINE__, __FUNCTION__, fmt, ##args)

/*
#ifdef KYLIN_DEBUG
#define DEBUG(fmt, args...)      LOG(DEBUG, fmt, ##args)
#define DEBUGV(fmt, args...)     LOG(MSG_DEBUG, fmt, ##args)
#else
#define DEBUG(fmt, args...)
#define DEBUGV(fmt, args...)
#endif
*/

const int kLogMaxRowLength = 8192;

template <typename LockType>
class ScopedLocker {
public:
    //explicit
    ScopedLocker(LockType& lock) : lock_(&lock) {
        lock_->Lock();
    }

    ScopedLocker(LockType* lock) : lock_(lock) {
        lock_->Lock();
    }

    ~ScopedLocker() {
        lock_->Unlock();
    }

private:
    LockType* lock_;
};

class MutexLock {
public:
    MutexLock() {
        pthread_mutex_init(&lock_, NULL);
    }

    ~MutexLock() {
        pthread_mutex_destroy(&lock_);
    }

    void Lock() {
        pthread_mutex_lock(&lock_);
    }

    void Unlock() {
        pthread_mutex_unlock(&lock_);
    }

private:
    pthread_mutex_t lock_;
};

class Log
{
public:
    static Log logger_;

public:
    Log(const std::string& path = "",
        const std::string& prefix = "",
        int level = LL_DEBUG,
        int max_file_count = 10);
    ~Log();

    void set_log_level(int level);
    int log_level() {return log_level_;}
    void set_max_file_count(int file_count);
    void set_need_process_id(bool value) { need_process_id_ = value; }
    void set_need_thread_id(bool value) { need_thread_id_ = value; }
    void set_rotate_by_day(bool value) { rotate_by_day_ = value; }

    bool SetLogPrefix(const std::string& path, const std::string& prefix);
    void Write(int level, const char *fmt, ...);
    void Write(int level, const char *filename, 
               int line, const char *function, 
               const char *fmt, ...);
    void Write(int level, const char *filename, 
               int line, const char *function, 
               const char *fmt, va_list args);

private:
    int CompareTm(const struct tm& left, const struct tm& right);
    std::string DefaultLogName();
    void MaybeCreateNewLog();
    void MaybeDeleteOldLogs();
    bool OpenLog(const std::string& new_log_name, int* fd);
    void CloseLog();
    void SetDefaultParam();
    std::string GetNewLogName(const tm& tm_now);
    int WriteData(const char *data, int size);
    bool GetFileList(const std::string& path, std::vector<std::string>* file_list);
    bool FileExists(const std::string& file_name);

    std::string path_;
    std::string prefix_;
    int fd_;
    int max_file_count_;
    int log_level_;
    bool need_process_id_;
    bool need_thread_id_;
    bool rotate_by_day_;
    
    struct tm current_tm_;
    std::list<std::string> exist_files_;
    MutexLock lock_;
};

#endif

